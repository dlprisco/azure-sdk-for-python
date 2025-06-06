# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
import sys
from typing import Any, AsyncIterator, Callable, Dict, IO, Optional, TypeVar, Union, cast, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    StreamClosedError,
    StreamConsumedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.polling import AsyncLROPoller, AsyncNoPolling, AsyncPollingMethod
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.async_arm_polling import AsyncARMPolling

from ... import models as _models
from ...operations._iot_hub_operations import build_manual_failover_request

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class IotHubOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.iothub.v2019_03_22.aio.IotHubClient`'s
        :attr:`iot_hub` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")
        self._api_version = input_args.pop(0) if input_args else kwargs.pop("api_version")

    async def _manual_failover_initial(
        self,
        iot_hub_name: str,
        resource_group_name: str,
        failover_input: Union[_models.FailoverInput, IO[bytes]],
        **kwargs: Any
    ) -> AsyncIterator[bytes]:
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2019-03-22"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[AsyncIterator[bytes]] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(failover_input, (IOBase, bytes)):
            _content = failover_input
        else:
            _json = self._serialize.body(failover_input, "FailoverInput")

        _request = build_manual_failover_request(
            iot_hub_name=iot_hub_name,
            resource_group_name=resource_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _decompress = kwargs.pop("decompress", True)
        _stream = True
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            try:
                await response.read()  # Load the body in memory and close the socket
            except (StreamConsumedError, StreamClosedError):
                pass
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorDetails, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = response.stream_download(self._client._pipeline, decompress=_decompress)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @overload
    async def begin_manual_failover(
        self,
        iot_hub_name: str,
        resource_group_name: str,
        failover_input: _models.FailoverInput,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Manually initiate a failover for the IoT Hub to its secondary region.

        Manually initiate a failover for the IoT Hub to its secondary region. To learn more, see
        https://aka.ms/manualfailover.

        :param iot_hub_name: Name of the IoT hub to failover. Required.
        :type iot_hub_name: str
        :param resource_group_name: Name of the resource group containing the IoT hub resource.
         Required.
        :type resource_group_name: str
        :param failover_input: Region to failover to. Must be the Azure paired region. Get the value
         from the secondary location in the locations property. To learn more, see
         https://aka.ms/manualfailover/region. Required.
        :type failover_input: ~azure.mgmt.iothub.v2019_03_22.models.FailoverInput
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def begin_manual_failover(
        self,
        iot_hub_name: str,
        resource_group_name: str,
        failover_input: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Manually initiate a failover for the IoT Hub to its secondary region.

        Manually initiate a failover for the IoT Hub to its secondary region. To learn more, see
        https://aka.ms/manualfailover.

        :param iot_hub_name: Name of the IoT hub to failover. Required.
        :type iot_hub_name: str
        :param resource_group_name: Name of the resource group containing the IoT hub resource.
         Required.
        :type resource_group_name: str
        :param failover_input: Region to failover to. Must be the Azure paired region. Get the value
         from the secondary location in the locations property. To learn more, see
         https://aka.ms/manualfailover/region. Required.
        :type failover_input: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def begin_manual_failover(
        self,
        iot_hub_name: str,
        resource_group_name: str,
        failover_input: Union[_models.FailoverInput, IO[bytes]],
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Manually initiate a failover for the IoT Hub to its secondary region.

        Manually initiate a failover for the IoT Hub to its secondary region. To learn more, see
        https://aka.ms/manualfailover.

        :param iot_hub_name: Name of the IoT hub to failover. Required.
        :type iot_hub_name: str
        :param resource_group_name: Name of the resource group containing the IoT hub resource.
         Required.
        :type resource_group_name: str
        :param failover_input: Region to failover to. Must be the Azure paired region. Get the value
         from the secondary location in the locations property. To learn more, see
         https://aka.ms/manualfailover/region. Is either a FailoverInput type or a IO[bytes] type.
         Required.
        :type failover_input: ~azure.mgmt.iothub.v2019_03_22.models.FailoverInput or IO[bytes]
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2019-03-22"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[None] = kwargs.pop("cls", None)
        polling: Union[bool, AsyncPollingMethod] = kwargs.pop("polling", True)
        lro_delay = kwargs.pop("polling_interval", self._config.polling_interval)
        cont_token: Optional[str] = kwargs.pop("continuation_token", None)
        if cont_token is None:
            raw_result = await self._manual_failover_initial(
                iot_hub_name=iot_hub_name,
                resource_group_name=resource_group_name,
                failover_input=failover_input,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x, y, z: x,
                headers=_headers,
                params=_params,
                **kwargs
            )
            await raw_result.http_response.read()  # type: ignore
        kwargs.pop("error_map", None)

        def get_long_running_output(pipeline_response):  # pylint: disable=inconsistent-return-statements
            if cls:
                return cls(pipeline_response, None, {})  # type: ignore

        if polling is True:
            polling_method: AsyncPollingMethod = cast(AsyncPollingMethod, AsyncARMPolling(lro_delay, **kwargs))
        elif polling is False:
            polling_method = cast(AsyncPollingMethod, AsyncNoPolling())
        else:
            polling_method = polling
        if cont_token:
            return AsyncLROPoller[None].from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output,
            )
        return AsyncLROPoller[None](self._client, raw_result, get_long_running_output, polling_method)  # type: ignore
