# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import


from ._models import (  # type: ignore
    Asset,
    AssetEndpointProfile,
    AssetEndpointProfileProperties,
    AssetEndpointProfileStatus,
    AssetEndpointProfileStatusError,
    AssetEndpointProfileUpdate,
    AssetEndpointProfileUpdateProperties,
    AssetProperties,
    AssetStatus,
    AssetStatusDataset,
    AssetStatusError,
    AssetStatusEvent,
    AssetUpdate,
    AssetUpdateProperties,
    Authentication,
    BillingContainer,
    BillingContainerProperties,
    DataPoint,
    DataPointBase,
    Dataset,
    ErrorAdditionalInfo,
    ErrorDetail,
    ErrorResponse,
    Event,
    EventBase,
    ExtendedLocation,
    MessageSchemaReference,
    Operation,
    OperationDisplay,
    OperationStatusResult,
    ProxyResource,
    Resource,
    SystemData,
    Topic,
    TrackedResource,
    UsernamePasswordCredentials,
    X509Credentials,
)

from ._enums import (  # type: ignore
    ActionType,
    AuthenticationMethod,
    CreatedByType,
    DataPointObservabilityMode,
    EventObservabilityMode,
    Origin,
    ProvisioningState,
    TopicRetainType,
)
from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "Asset",
    "AssetEndpointProfile",
    "AssetEndpointProfileProperties",
    "AssetEndpointProfileStatus",
    "AssetEndpointProfileStatusError",
    "AssetEndpointProfileUpdate",
    "AssetEndpointProfileUpdateProperties",
    "AssetProperties",
    "AssetStatus",
    "AssetStatusDataset",
    "AssetStatusError",
    "AssetStatusEvent",
    "AssetUpdate",
    "AssetUpdateProperties",
    "Authentication",
    "BillingContainer",
    "BillingContainerProperties",
    "DataPoint",
    "DataPointBase",
    "Dataset",
    "ErrorAdditionalInfo",
    "ErrorDetail",
    "ErrorResponse",
    "Event",
    "EventBase",
    "ExtendedLocation",
    "MessageSchemaReference",
    "Operation",
    "OperationDisplay",
    "OperationStatusResult",
    "ProxyResource",
    "Resource",
    "SystemData",
    "Topic",
    "TrackedResource",
    "UsernamePasswordCredentials",
    "X509Credentials",
    "ActionType",
    "AuthenticationMethod",
    "CreatedByType",
    "DataPointObservabilityMode",
    "EventObservabilityMode",
    "Origin",
    "ProvisioningState",
    "TopicRetainType",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
