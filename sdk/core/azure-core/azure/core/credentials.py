# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
from typing import Any, NamedTuple, Optional, TypedDict, Union, ContextManager
from typing_extensions import Protocol, runtime_checkable


class AccessToken(NamedTuple):
    """Represents an OAuth access token."""

    token: str
    """The token string."""
    expires_on: int
    """The token's expiration time in Unix time."""


class AccessTokenInfo:
    """Information about an OAuth access token.

    This class is an alternative to `AccessToken` which provides additional information about the token.

    :param str token: The token string.
    :param int expires_on: The token's expiration time in Unix time.
    :keyword str token_type: The type of access token. Defaults to 'Bearer'.
    :keyword int refresh_on: Specifies the time, in Unix time, when the cached token should be proactively
        refreshed. Optional.
    """

    token: str
    """The token string."""
    expires_on: int
    """The token's expiration time in Unix time."""
    token_type: str
    """The type of access token."""
    refresh_on: Optional[int]
    """Specifies the time, in Unix time, when the cached token should be proactively refreshed. Optional."""

    def __init__(
        self,
        token: str,
        expires_on: int,
        *,
        token_type: str = "Bearer",
        refresh_on: Optional[int] = None,
    ) -> None:
        self.token = token
        self.expires_on = expires_on
        self.token_type = token_type
        self.refresh_on = refresh_on

    def __repr__(self) -> str:
        return "AccessTokenInfo(token='{}', expires_on={}, token_type='{}', refresh_on={})".format(
            self.token, self.expires_on, self.token_type, self.refresh_on
        )


class TokenRequestOptions(TypedDict, total=False):
    """Options to use for access token requests. All parameters are optional."""

    claims: str
    """Additional claims required in the token, such as those returned in a resource provider's claims
    challenge following an authorization failure."""
    tenant_id: str
    """The tenant ID to include in the token request."""
    enable_cae: bool
    """Indicates whether to enable Continuous Access Evaluation (CAE) for the requested token."""


@runtime_checkable
class TokenCredential(Protocol):
    """Protocol for classes able to provide OAuth tokens."""

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        enable_cae: bool = False,
        **kwargs: Any,
    ) -> AccessToken:
        """Request an access token for `scopes`.

        :param str scopes: The type of access needed.

        :keyword str claims: Additional claims required in the token, such as those returned in a resource
            provider's claims challenge following an authorization failure.
        :keyword str tenant_id: Optional tenant to include in the token request.
        :keyword bool enable_cae: Indicates whether to enable Continuous Access Evaluation (CAE) for the requested
            token. Defaults to False.

        :rtype: AccessToken
        :return: An AccessToken instance containing the token string and its expiration time in Unix time.
        """
        ...


@runtime_checkable
class SupportsTokenInfo(Protocol, ContextManager["SupportsTokenInfo"]):
    """Protocol for classes able to provide OAuth access tokens with additional properties."""

    def get_token_info(self, *scopes: str, options: Optional[TokenRequestOptions] = None) -> AccessTokenInfo:
        """Request an access token for `scopes`.

        This is an alternative to `get_token` to enable certain scenarios that require additional properties
        on the token.

        :param str scopes: The type of access needed.
        :keyword options: A dictionary of options for the token request. Unknown options will be ignored. Optional.
        :paramtype options: TokenRequestOptions

        :rtype: AccessTokenInfo
        :return: An AccessTokenInfo instance containing information about the token.
        """
        ...

    def close(self) -> None:
        """Close the credential, releasing any resources it holds.

        :return: None
        :rtype: None
        """


TokenProvider = Union[TokenCredential, SupportsTokenInfo]


class AzureNamedKey(NamedTuple):
    """Represents a name and key pair."""

    name: str
    key: str


__all__ = [
    "AzureKeyCredential",
    "AzureSasCredential",
    "AccessToken",
    "AccessTokenInfo",
    "SupportsTokenInfo",
    "AzureNamedKeyCredential",
    "TokenCredential",
    "TokenRequestOptions",
    "TokenProvider",
]


class AzureKeyCredential:
    """Credential type used for authenticating to an Azure service.
    It provides the ability to update the key without creating a new client.

    :param str key: The key used to authenticate to an Azure service
    :raises TypeError: If the key is not a string.
    """

    def __init__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string.")
        self._key = key

    @property
    def key(self) -> str:
        """The value of the configured key.

        :rtype: str
        :return: The value of the configured key.
        """
        return self._key

    def update(self, key: str) -> None:
        """Update the key.

        This can be used when you've regenerated your service key and want
        to update long-lived clients.

        :param str key: The key used to authenticate to an Azure service
        :raises ValueError or TypeError: If the key is None, empty, or not a string.
        """
        if not key:
            raise ValueError("The key used for updating can not be None or empty")
        if not isinstance(key, str):
            raise TypeError("The key used for updating must be a string.")
        self._key = key


class AzureSasCredential:
    """Credential type used for authenticating to an Azure service.
    It provides the ability to update the shared access signature without creating a new client.

    :param str signature: The shared access signature used to authenticate to an Azure service
    :raises TypeError: If the signature is not a string.
    """

    def __init__(self, signature: str) -> None:
        if not isinstance(signature, str):
            raise TypeError("signature must be a string.")
        self._signature = signature

    @property
    def signature(self) -> str:
        """The value of the configured shared access signature.

        :rtype: str
        :return: The value of the configured shared access signature.
        """
        return self._signature

    def update(self, signature: str) -> None:
        """Update the shared access signature.

        This can be used when you've regenerated your shared access signature and want
        to update long-lived clients.

        :param str signature: The shared access signature used to authenticate to an Azure service
        :raises ValueError: If the signature is None or empty.
        :raises TypeError: If the signature is not a string.
        """
        if not signature:
            raise ValueError("The signature used for updating can not be None or empty")
        if not isinstance(signature, str):
            raise TypeError("The signature used for updating must be a string.")
        self._signature = signature


class AzureNamedKeyCredential:
    """Credential type used for working with any service needing a named key that follows patterns
    established by the other credential types.

    :param str name: The name of the credential used to authenticate to an Azure service.
    :param str key: The key used to authenticate to an Azure service.
    :raises TypeError: If the name or key is not a string.
    """

    def __init__(self, name: str, key: str) -> None:
        if not isinstance(name, str) or not isinstance(key, str):
            raise TypeError("Both name and key must be strings.")
        self._credential = AzureNamedKey(name, key)

    @property
    def named_key(self) -> AzureNamedKey:
        """The value of the configured name.

        :rtype: AzureNamedKey
        :return: The value of the configured name.
        """
        return self._credential

    def update(self, name: str, key: str) -> None:
        """Update the named key credential.

        Both name and key must be provided in order to update the named key credential.
        Individual attributes cannot be updated.

        :param str name: The name of the credential used to authenticate to an Azure service.
        :param str key: The key used to authenticate to an Azure service.
        """
        if not isinstance(name, str) or not isinstance(key, str):
            raise TypeError("Both name and key must be strings.")
        self._credential = AzureNamedKey(name, key)
