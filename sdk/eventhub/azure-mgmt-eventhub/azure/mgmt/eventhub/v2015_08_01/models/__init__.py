# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import


from ._models_py3 import (  # type: ignore
    CheckNameAvailabilityParameter,
    CheckNameAvailabilityResult,
    ConsumerGroupCreateOrUpdateParameters,
    ConsumerGroupListResult,
    ConsumerGroupResource,
    EventHubCreateOrUpdateParameters,
    EventHubListResult,
    EventHubResource,
    NamespaceCreateOrUpdateParameters,
    NamespaceListResult,
    NamespaceResource,
    NamespaceUpdateParameter,
    Operation,
    OperationDisplay,
    OperationListResult,
    RegenerateKeysParameters,
    Resource,
    ResourceListKeys,
    SharedAccessAuthorizationRuleCreateOrUpdateParameters,
    SharedAccessAuthorizationRuleListResult,
    SharedAccessAuthorizationRuleResource,
    Sku,
    TrackedResource,
)

from ._event_hub_management_client_enums import (  # type: ignore
    AccessRights,
    EntityStatus,
    NamespaceState,
    Policykey,
    SkuName,
    SkuTier,
    UnavailableReason,
)
from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "CheckNameAvailabilityParameter",
    "CheckNameAvailabilityResult",
    "ConsumerGroupCreateOrUpdateParameters",
    "ConsumerGroupListResult",
    "ConsumerGroupResource",
    "EventHubCreateOrUpdateParameters",
    "EventHubListResult",
    "EventHubResource",
    "NamespaceCreateOrUpdateParameters",
    "NamespaceListResult",
    "NamespaceResource",
    "NamespaceUpdateParameter",
    "Operation",
    "OperationDisplay",
    "OperationListResult",
    "RegenerateKeysParameters",
    "Resource",
    "ResourceListKeys",
    "SharedAccessAuthorizationRuleCreateOrUpdateParameters",
    "SharedAccessAuthorizationRuleListResult",
    "SharedAccessAuthorizationRuleResource",
    "Sku",
    "TrackedResource",
    "AccessRights",
    "EntityStatus",
    "NamespaceState",
    "Policykey",
    "SkuName",
    "SkuTier",
    "UnavailableReason",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
