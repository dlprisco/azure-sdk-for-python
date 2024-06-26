# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._group_quotas_operations import GroupQuotasOperations
from ._group_quota_subscriptions_operations import GroupQuotaSubscriptionsOperations
from ._group_quota_subscription_requests_operations import GroupQuotaSubscriptionRequestsOperations
from ._group_quota_limits_operations import GroupQuotaLimitsOperations
from ._group_quota_limits_request_operations import GroupQuotaLimitsRequestOperations
from ._group_quota_subscription_allocation_operations import GroupQuotaSubscriptionAllocationOperations
from ._group_quota_subscription_allocation_request_operations import GroupQuotaSubscriptionAllocationRequestOperations
from ._group_quota_usages_operations import GroupQuotaUsagesOperations
from ._group_quota_location_settings_operations import GroupQuotaLocationSettingsOperations
from ._usages_operations import UsagesOperations
from ._quota_operations import QuotaOperations
from ._quota_request_status_operations import QuotaRequestStatusOperations
from ._quota_operation_operations import QuotaOperationOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "GroupQuotasOperations",
    "GroupQuotaSubscriptionsOperations",
    "GroupQuotaSubscriptionRequestsOperations",
    "GroupQuotaLimitsOperations",
    "GroupQuotaLimitsRequestOperations",
    "GroupQuotaSubscriptionAllocationOperations",
    "GroupQuotaSubscriptionAllocationRequestOperations",
    "GroupQuotaUsagesOperations",
    "GroupQuotaLocationSettingsOperations",
    "UsagesOperations",
    "QuotaOperations",
    "QuotaRequestStatusOperations",
    "QuotaOperationOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
