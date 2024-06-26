# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class AccountCreationSource(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Source of Account creation."""

    LIFTR = "LIFTR"
    """Account is created from LIFTR"""
    NEWRELIC = "NEWRELIC"
    """Account is created from NEWRELIC"""


class ActionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum. Indicates the action type. "Internal" refers to actions that are for internal only APIs."""

    INTERNAL = "Internal"


class BillingCycle(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Different usage type like YEARLY/MONTHLY."""

    YEARLY = "YEARLY"
    """Billing cycle is YEARLY"""
    MONTHLY = "MONTHLY"
    """Billing cycle is MONTHLY"""
    WEEKLY = "WEEKLY"
    """Billing cycle is WEEKLY"""


class BillingSource(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Billing source."""

    AZURE = "AZURE"
    """Billing source is Azure"""
    NEWRELIC = "NEWRELIC"


class ConfigurationName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """ConfigurationName."""

    DEFAULT = "default"


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class LiftrResourceCategories(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Liftr Resource category."""

    UNKNOWN = "Unknown"
    MONITOR_LOGS = "MonitorLogs"


class ManagedServiceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of managed service identity (where both SystemAssigned and UserAssigned types are
    allowed).
    """

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"


class MarketplaceSubscriptionStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Flag specifying the Marketplace Subscription Status of the resource. If payment is not made in
    time, the resource will go in Suspended state.
    """

    ACTIVE = "Active"
    """monitoring is enabled"""
    SUSPENDED = "Suspended"
    """monitoring is disabled"""


class MonitoringStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Flag specifying if the resource monitoring is enabled or disabled."""

    ENABLED = "Enabled"
    """monitoring is enabled"""
    DISABLED = "Disabled"
    """monitoring is disabled"""


class OrgCreationSource(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Source of Org creation."""

    LIFTR = "LIFTR"
    """Org is created from LIFTR"""
    NEWRELIC = "NEWRELIC"
    """Org is created from NEWRELIC"""


class Origin(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The intended executor of the operation; as in Resource Based Access Control (RBAC) and audit
    logs UX. Default value is "user,system".
    """

    USER = "user"
    SYSTEM = "system"
    USER_SYSTEM = "user,system"


class PatchOperation(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The operation for the patch on the resource."""

    ADD_BEGIN = "AddBegin"
    ADD_COMPLETE = "AddComplete"
    DELETE_BEGIN = "DeleteBegin"
    DELETE_COMPLETE = "DeleteComplete"
    ACTIVE = "Active"


class ProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Provisioning State of the Monitor resource."""

    ACCEPTED = "Accepted"
    """Monitor resource creation request accepted"""
    CREATING = "Creating"
    """Monitor resource creation started"""
    UPDATING = "Updating"
    """Monitor resource is being updated"""
    DELETING = "Deleting"
    """Monitor resource deletion started"""
    SUCCEEDED = "Succeeded"
    """Monitor resource creation successful"""
    FAILED = "Failed"
    """Monitor resource creation failed"""
    CANCELED = "Canceled"
    """Monitor resource creation canceled"""
    DELETED = "Deleted"
    """Monitor resource is deleted"""
    NOT_SPECIFIED = "NotSpecified"
    """Monitor resource state is unknown"""


class SendAadLogsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether AAD logs are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SendActivityLogsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether activity logs are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SendingLogsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether logs are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SendingMetricsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether metrics are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SendMetricsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether metrics are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SendSubscriptionLogsStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Indicates whether subscription logs are being sent."""

    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SingleSignOnStates(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Various states of the SSO resource."""

    INITIAL = "Initial"
    ENABLE = "Enable"
    DISABLE = "Disable"
    EXISTING = "Existing"


class Status(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The state of monitoring."""

    IN_PROGRESS = "InProgress"
    ACTIVE = "Active"
    FAILED = "Failed"
    DELETING = "Deleting"


class TagAction(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Valid actions for a filtering tag. Exclusion takes priority over inclusion."""

    INCLUDE = "Include"
    EXCLUDE = "Exclude"


class UsageType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Different usage type like PAYG/COMMITTED."""

    PAYG = "PAYG"
    """Usage type is PAYG"""
    COMMITTED = "COMMITTED"
    """Usage type is COMMITTED"""
