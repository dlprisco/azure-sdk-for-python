# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
import os
from typing import Optional, Dict

from azure.core.pipeline.transport import HttpRequest

from .._constants import EnvironmentVariables
from .._internal.msal_managed_identity_client import MsalManagedIdentityClient


class AzureMLCredential(MsalManagedIdentityClient):
    def get_unavailable_message(self, desc: str = "") -> str:
        return f"Azure ML managed identity configuration not found in environment. {desc}"


def _get_client_args(**kwargs) -> Optional[Dict]:
    identity_config = kwargs.pop("identity_config", None) or {}

    url = os.environ.get(EnvironmentVariables.MSI_ENDPOINT)
    secret = os.environ.get(EnvironmentVariables.MSI_SECRET)
    if not (url and secret):
        # Azure ML managed identity isn't available in this environment
        return None

    if kwargs.get("client_id"):
        identity_config["clientid"] = kwargs.pop("client_id")

    return dict(
        kwargs,
        _content_callback=_parse_expires_on,
        identity_config=identity_config,
        base_headers={"secret": secret},
        request_factory=functools.partial(_get_request, url),
    )


def _get_request(url: str, scope: str, identity_config: Dict) -> HttpRequest:
    request = HttpRequest("GET", url)
    request.format_parameters(dict({"api-version": "2017-09-01", "resource": scope}, **identity_config))
    return request


def _parse_expires_on(content: Dict) -> None:
    """Parse an App Service MSI version 2017-09-01 expires_on value to epoch seconds.

    This version of the API returns expires_on as a UTC datetime string rather than epoch seconds. The string's
    format depends on the OS. Responses on Windows include AM/PM, for example "1/16/2020 5:24:12 AM +00:00".
    Responses on Linux do not, for example "06/20/2019 02:57:58 +00:00".

    :param dict content: a deserialized response from an App Service MSI.
    :raises ValueError: ``expires_on`` didn't match an expected format
    """

    # Azure ML sets the same environment variables as App Service but returns expires_on as an integer.
    # That means we could have an Azure ML response here, so let's first try to parse expires_on as an int.
    try:
        content["expires_on"] = int(content["expires_on"])
        return
    except ValueError:
        pass

    import calendar
    import time

    expires_on = content["expires_on"]
    if expires_on.endswith(" +00:00"):
        date_string = expires_on[: -len(" +00:00")]
        for format_string in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y %I:%M:%S %p"):  # (Linux, Windows)
            try:
                t = time.strptime(date_string, format_string)
                content["expires_on"] = calendar.timegm(t)
                return
            except ValueError:
                pass

    raise ValueError("'{}' doesn't match the expected format".format(expires_on))
