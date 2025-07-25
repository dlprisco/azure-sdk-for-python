# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
import time
import base64
from typing import Any, Awaitable, Optional, cast, TypeVar, Union

from azure.core.credentials import AccessToken, AccessTokenInfo, TokenRequestOptions
from azure.core.credentials_async import (
    AsyncTokenCredential,
    AsyncSupportsTokenInfo,
    AsyncTokenProvider,
)
from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.policies import AsyncHTTPPolicy
from azure.core.pipeline.policies._authentication import (
    _BearerTokenCredentialPolicyBase,
)
from azure.core.pipeline.transport import (
    AsyncHttpResponse as LegacyAsyncHttpResponse,
    HttpRequest as LegacyHttpRequest,
)
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.utils._utils import get_running_async_lock
from ._utils import get_challenge_parameter

from .._tools_async import await_result

AsyncHTTPResponseType = TypeVar("AsyncHTTPResponseType", AsyncHttpResponse, LegacyAsyncHttpResponse)
HTTPRequestType = TypeVar("HTTPRequestType", HttpRequest, LegacyHttpRequest)


class AsyncBearerTokenCredentialPolicy(AsyncHTTPPolicy[HTTPRequestType, AsyncHTTPResponseType]):
    """Adds a bearer token Authorization header to requests.

    :param credential: The credential.
    :type credential: ~azure.core.credentials_async.AsyncTokenProvider
    :param str scopes: Lets you specify the type of access needed.
    :keyword bool enable_cae: Indicates whether to enable Continuous Access Evaluation (CAE) on all requested
        tokens. Defaults to False.
    """

    def __init__(self, credential: AsyncTokenProvider, *scopes: str, **kwargs: Any) -> None:
        super().__init__()
        self._credential = credential
        self._scopes = scopes
        self._lock_instance = None
        self._token: Optional[Union["AccessToken", "AccessTokenInfo"]] = None
        self._enable_cae: bool = kwargs.get("enable_cae", False)

    @property
    def _lock(self):
        if self._lock_instance is None:
            self._lock_instance = get_running_async_lock()
        return self._lock_instance

    async def on_request(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Adds a bearer token Authorization header to request and sends request to next policy.

        :param request: The pipeline request object to be modified.
        :type request: ~azure.core.pipeline.PipelineRequest
        :raises ~azure.core.exceptions.ServiceRequestError: If the request fails.
        """
        _BearerTokenCredentialPolicyBase._enforce_https(request)  # pylint:disable=protected-access

        if self._token is None or self._need_new_token():
            async with self._lock:
                # double check because another coroutine may have acquired a token while we waited to acquire the lock
                if self._token is None or self._need_new_token():
                    await self._request_token(*self._scopes)
        bearer_token = cast(Union[AccessToken, AccessTokenInfo], self._token).token
        request.http_request.headers["Authorization"] = "Bearer " + bearer_token

    async def authorize_request(self, request: PipelineRequest[HTTPRequestType], *scopes: str, **kwargs: Any) -> None:
        """Acquire a token from the credential and authorize the request with it.

        Keyword arguments are passed to the credential's get_token method. The token will be cached and used to
        authorize future requests.

        :param ~azure.core.pipeline.PipelineRequest request: the request
        :param str scopes: required scopes of authentication
        """

        async with self._lock:
            await self._request_token(*scopes, **kwargs)
        bearer_token = cast(Union[AccessToken, AccessTokenInfo], self._token).token
        request.http_request.headers["Authorization"] = "Bearer " + bearer_token

    async def send(
        self, request: PipelineRequest[HTTPRequestType]
    ) -> PipelineResponse[HTTPRequestType, AsyncHTTPResponseType]:
        """Authorize request with a bearer token and send it to the next policy

        :param request: The pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        :return: The pipeline response object
        :rtype: ~azure.core.pipeline.PipelineResponse
        """
        await await_result(self.on_request, request)
        response: PipelineResponse[HTTPRequestType, AsyncHTTPResponseType]
        try:
            response = await self.next.send(request)
        except Exception:
            await await_result(self.on_exception, request)
            raise
        await await_result(self.on_response, request, response)

        if response.http_response.status_code == 401:
            self._token = None  # any cached token is invalid
            if "WWW-Authenticate" in response.http_response.headers:
                request_authorized = await self.on_challenge(request, response)
                if request_authorized:
                    # if we receive a challenge response, we retrieve a new token
                    # which matches the new target. In this case, we don't want to remove
                    # token from the request so clear the 'insecure_domain_change' tag
                    request.context.options.pop("insecure_domain_change", False)
                    try:
                        response = await self.next.send(request)
                    except Exception:
                        await await_result(self.on_exception, request)
                        raise
                    await await_result(self.on_response, request, response)

        return response

    async def on_challenge(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: PipelineResponse[HTTPRequestType, AsyncHTTPResponseType],
    ) -> bool:
        """Authorize request according to an authentication challenge

        This method is called when the resource provider responds 401 with a WWW-Authenticate header.

        :param ~azure.core.pipeline.PipelineRequest request: the request which elicited an authentication challenge
        :param ~azure.core.pipeline.PipelineResponse response: the resource provider's response
        :returns: a bool indicating whether the policy should send the request
        :rtype: bool
        """
        headers = response.http_response.headers
        error = get_challenge_parameter(headers, "Bearer", "error")
        if error == "insufficient_claims":
            encoded_claims = get_challenge_parameter(headers, "Bearer", "claims")
            if not encoded_claims:
                return False
            try:
                padding_needed = -len(encoded_claims) % 4
                claims = base64.urlsafe_b64decode(encoded_claims + "=" * padding_needed).decode("utf-8")
                if claims:
                    await self.authorize_request(request, *self._scopes, claims=claims)
                    return True
            except Exception:  # pylint:disable=broad-except
                return False
        return False

    def on_response(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: PipelineResponse[HTTPRequestType, AsyncHTTPResponseType],
    ) -> Optional[Awaitable[None]]:
        """Executed after the request comes back from the next policy.

        :param request: Request to be modified after returning from the policy.
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: Pipeline response object
        :type response: ~azure.core.pipeline.PipelineResponse
        """

    def on_exception(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Executed when an exception is raised while executing the next policy.

        This method is executed inside the exception handler.

        :param request: The Pipeline request object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        # pylint: disable=unused-argument
        return

    def _need_new_token(self) -> bool:
        now = time.time()
        refresh_on = getattr(self._token, "refresh_on", None)
        return not self._token or (refresh_on and refresh_on <= now) or self._token.expires_on - now < 300

    async def _get_token(self, *scopes: str, **kwargs: Any) -> Union["AccessToken", "AccessTokenInfo"]:
        if self._enable_cae:
            kwargs.setdefault("enable_cae", self._enable_cae)

        if hasattr(self._credential, "get_token_info"):
            options: TokenRequestOptions = {}
            # Loop through all the keyword arguments and check if they are part of the TokenRequestOptions.
            for key in list(kwargs.keys()):
                if key in TokenRequestOptions.__annotations__:  # pylint: disable=no-member
                    options[key] = kwargs.pop(key)  # type: ignore[literal-required]

            return await await_result(
                cast(AsyncSupportsTokenInfo, self._credential).get_token_info,
                *scopes,
                options=options,
            )
        return await await_result(
            cast(AsyncTokenCredential, self._credential).get_token,
            *scopes,
            **kwargs,
        )

    async def _request_token(self, *scopes: str, **kwargs: Any) -> None:
        """Request a new token from the credential.

        This will call the credential's appropriate method to get a token and store it in the policy.

        :param str scopes: The type of access needed.
        """
        self._token = await self._get_token(*scopes, **kwargs)
