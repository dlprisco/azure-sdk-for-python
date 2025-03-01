# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from enum import Enum

from azure.ai.ml._utils._experimental import experimental
from azure.core import CaseInsensitiveEnumMeta


class ManagedServiceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of managed service identity (where both SystemAssigned and UserAssigned types are allowed)."""

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"


class IsolationMode:
    """IsolationMode for the workspace managed network."""

    DISABLED = "Disabled"
    ALLOW_INTERNET_OUTBOUND = "AllowInternetOutbound"
    ALLOW_ONLY_APPROVED_OUTBOUND = "AllowOnlyApprovedOutbound"


@experimental
class FirewallSku:
    """Firewall Sku for FQDN rules in AllowOnlyApprovedOutbound."""

    STANDARD = "Standard"
    BASIC = "Basic"


class OutboundRuleCategory:
    """Category for a managed network outbound rule."""

    REQUIRED = "Required"
    RECOMMENDED = "Recommended"
    USER_DEFINED = "UserDefined"
    DEPENDENCY = "Dependency"


class OutboundRuleType:
    """Type of managed network outbound rule."""

    FQDN = "FQDN"
    PRIVATE_ENDPOINT = "PrivateEndpoint"
    SERVICE_TAG = "ServiceTag"


@experimental
class CapabilityHostKind(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Capabilityhost kind."""

    AGENTS = "Agents"
