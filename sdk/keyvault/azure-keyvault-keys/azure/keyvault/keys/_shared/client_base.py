# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from copy import deepcopy
from enum import Enum
from typing import Any
from urllib.parse import urlparse

from azure.core import CaseInsensitiveEnumMeta
from azure.core.credentials import TokenCredential
from azure.core.pipeline.policies import HttpLoggingPolicy
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator import distributed_trace

from . import ChallengeAuthPolicy
from .._generated import KeyVaultClient as _KeyVaultClient
from .._generated import models as _models
from .._generated._utils.serialization import Serializer
from .._sdk_moniker import SDK_MONIKER


class ApiVersion(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Key Vault API versions supported by this package"""

    #: this is the default version
    V7_6 = "7.6"
    V7_5 = "7.5"
    V7_4 = "7.4"
    V7_3 = "7.3"
    V7_2 = "7.2"
    V7_1 = "7.1"
    V7_0 = "7.0"
    V2016_10_01 = "2016-10-01"


DEFAULT_VERSION = ApiVersion.V7_6

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def _format_api_version(request: HttpRequest, api_version: str) -> HttpRequest:
    """Returns a request copy that includes an api-version query parameter if one wasn't originally present.

    :param request: The HTTP request being sent.
    :type request: ~azure.core.rest.HttpRequest
    :param str api_version: The service API version that the request should include.

    :returns: A copy of the request that includes an api-version query parameter.
    :rtype: azure.core.rest.HttpRequest
    """
    request_copy = deepcopy(request)
    params = {"api-version": api_version}  # By default, we want to use the client's API version
    query = urlparse(request_copy.url).query

    if query:
        request_copy.url = request_copy.url.partition("?")[0]
        existing_params = {p[0]: p[-1] for p in [p.partition("=") for p in query.split("&")]}
        params.update(existing_params)  # If an api-version was provided, this will overwrite our default

    # Reconstruct the query parameters onto the URL
    query_params = []
    for k, v in params.items():
        query_params.append("{}={}".format(k, v))
    query = "?" + "&".join(query_params)
    request_copy.url = request_copy.url + query
    return request_copy


class KeyVaultClientBase(object):
    # pylint:disable=protected-access
    def __init__(self, vault_url: str, credential: TokenCredential, **kwargs: Any) -> None:
        if not credential:
            raise ValueError(
                "credential should be an object supporting the TokenCredential protocol, "
                "such as a credential from azure-identity"
            )
        if not vault_url:
            raise ValueError("vault_url must be the URL of an Azure Key Vault")

        try:
            self.api_version = kwargs.pop("api_version", DEFAULT_VERSION)
            # If API version was provided as an enum value, need to make a plain string for 3.11 compatibility
            if hasattr(self.api_version, "value"):
                self.api_version = self.api_version.value
            self._vault_url = vault_url.strip(" /")

            client = kwargs.get("generated_client")
            if client:
                # caller provided a configured client -> only models left to initialize
                self._client = client
                models = kwargs.get("generated_models")
                self._models = models or _models
                return

            http_logging_policy = HttpLoggingPolicy(**kwargs)
            http_logging_policy.allowed_header_names.update(
                {"x-ms-keyvault-network-info", "x-ms-keyvault-region", "x-ms-keyvault-service-version"}
            )

            verify_challenge = kwargs.pop("verify_challenge_resource", True)
            self._client = _KeyVaultClient(
                credential=credential,
                vault_base_url=self._vault_url,
                api_version=self.api_version,
                authentication_policy=ChallengeAuthPolicy(credential, verify_challenge_resource=verify_challenge),
                sdk_moniker=SDK_MONIKER,
                http_logging_policy=http_logging_policy,
                **kwargs
            )
            self._models = _models
        except ValueError as exc:
            # Ignore pyright error that comes from not identifying ApiVersion as an iterable enum
            raise NotImplementedError(
                f"This package doesn't support API version '{self.api_version}'. "
                + "Supported versions: "
                + f"{', '.join(v.value for v in ApiVersion)}"  # pyright: ignore[reportGeneralTypeIssues]
            ) from exc

    @property
    def vault_url(self) -> str:
        return self._vault_url

    def __enter__(self) -> "KeyVaultClientBase":
        self._client.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._client.__exit__(*args)

    def close(self) -> None:
        """Close sockets opened by the client.

        Calling this method is unnecessary when using the client as a context manager.
        """
        self._client.close()

    @distributed_trace
    def send_request(self, request: HttpRequest, *, stream: bool = False, **kwargs: Any) -> HttpResponse:
        """Runs a network request using the client's existing pipeline.

        The request URL can be relative to the vault URL. The service API version used for the request is the same as
        the client's unless otherwise specified. This method does not raise if the response is an error; to raise an
        exception, call `raise_for_status()` on the returned response object. For more information about how to send
        custom requests with this method, see https://aka.ms/azsdk/dpcodegen/python/send_request.

        :param request: The network request you want to make.
        :type request: ~azure.core.rest.HttpRequest

        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.

        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.HttpResponse
        """
        request_copy = _format_api_version(request, self.api_version)
        path_format_arguments = {
            "vaultBaseUrl": _SERIALIZER.url("vault_base_url", self._vault_url, "str", skip_quote=True),
        }
        request_copy.url = self._client._client.format_url(request_copy.url, **path_format_arguments)
        return self._client._client.send_request(request_copy, stream=stream, **kwargs)
