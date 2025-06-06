# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.network.aio import NetworkManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestNetworkManagementVirtualHubsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(NetworkManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_get(self, resource_group):
        response = await self.client.virtual_hubs.get(
            resource_group_name=resource_group.name,
            virtual_hub_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_begin_create_or_update(self, resource_group):
        response = await (
            await self.client.virtual_hubs.begin_create_or_update(
                resource_group_name=resource_group.name,
                virtual_hub_name="str",
                virtual_hub_parameters={
                    "addressPrefix": "str",
                    "allowBranchToBranchTraffic": bool,
                    "azureFirewall": {"id": "str"},
                    "bgpConnections": [{"id": "str"}],
                    "etag": "str",
                    "expressRouteGateway": {"id": "str"},
                    "hubRoutingPreference": "str",
                    "id": "str",
                    "ipConfigurations": [{"id": "str"}],
                    "kind": "str",
                    "location": "str",
                    "name": "str",
                    "p2SVpnGateway": {"id": "str"},
                    "preferredRoutingGateway": "str",
                    "provisioningState": "str",
                    "routeMaps": [{"id": "str"}],
                    "routeTable": {"routes": [{"addressPrefixes": ["str"], "nextHopIpAddress": "str"}]},
                    "routingState": "str",
                    "securityPartnerProvider": {"id": "str"},
                    "securityProviderName": "str",
                    "sku": "str",
                    "tags": {"str": "str"},
                    "type": "str",
                    "virtualHubRouteTableV2s": [
                        {
                            "attachedConnections": ["str"],
                            "etag": "str",
                            "id": "str",
                            "name": "str",
                            "provisioningState": "str",
                            "routes": [
                                {
                                    "destinationType": "str",
                                    "destinations": ["str"],
                                    "nextHopType": "str",
                                    "nextHops": ["str"],
                                }
                            ],
                        }
                    ],
                    "virtualRouterAsn": 0,
                    "virtualRouterAutoScaleConfiguration": {"minCapacity": 0},
                    "virtualRouterIps": ["str"],
                    "virtualWan": {"id": "str"},
                    "vpnGateway": {"id": "str"},
                },
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_update_tags(self, resource_group):
        response = await self.client.virtual_hubs.update_tags(
            resource_group_name=resource_group.name,
            virtual_hub_name="str",
            virtual_hub_parameters={"tags": {"str": "str"}},
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_begin_delete(self, resource_group):
        response = await (
            await self.client.virtual_hubs.begin_delete(
                resource_group_name=resource_group.name,
                virtual_hub_name="str",
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_list_by_resource_group(self, resource_group):
        response = self.client.virtual_hubs.list_by_resource_group(
            resource_group_name=resource_group.name,
            api_version="2024-07-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_list(self, resource_group):
        response = self.client.virtual_hubs.list(
            api_version="2024-07-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_begin_get_effective_virtual_hub_routes(self, resource_group):
        response = await (
            await self.client.virtual_hubs.begin_get_effective_virtual_hub_routes(
                resource_group_name=resource_group.name,
                virtual_hub_name="str",
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_begin_get_inbound_routes(self, resource_group):
        response = await (
            await self.client.virtual_hubs.begin_get_inbound_routes(
                resource_group_name=resource_group.name,
                virtual_hub_name="str",
                get_inbound_routes_parameters={"connectionType": "str", "resourceUri": "str"},
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_virtual_hubs_begin_get_outbound_routes(self, resource_group):
        response = await (
            await self.client.virtual_hubs.begin_get_outbound_routes(
                resource_group_name=resource_group.name,
                virtual_hub_name="str",
                get_outbound_routes_parameters={"connectionType": "str", "resourceUri": "str"},
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
