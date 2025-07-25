# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.appconfiguration import AppConfigurationManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestAppConfigurationManagementReplicasOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(AppConfigurationManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replicas_list_by_configuration_store(self, resource_group):
        response = self.client.replicas.list_by_configuration_store(
            resource_group_name=resource_group.name,
            config_store_name="str",
            api_version="2024-06-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replicas_get(self, resource_group):
        response = self.client.replicas.get(
            resource_group_name=resource_group.name,
            config_store_name="str",
            replica_name="str",
            api_version="2024-06-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replicas_begin_create(self, resource_group):
        response = self.client.replicas.begin_create(
            resource_group_name=resource_group.name,
            config_store_name="str",
            replica_name="str",
            replica_creation_parameters={
                "endpoint": "str",
                "id": "str",
                "location": "str",
                "name": "str",
                "provisioningState": "str",
                "systemData": {
                    "createdAt": "2020-02-20 00:00:00",
                    "createdBy": "str",
                    "createdByType": "str",
                    "lastModifiedAt": "2020-02-20 00:00:00",
                    "lastModifiedBy": "str",
                    "lastModifiedByType": "str",
                },
                "type": "str",
            },
            api_version="2024-06-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replicas_begin_delete(self, resource_group):
        response = self.client.replicas.begin_delete(
            resource_group_name=resource_group.name,
            config_store_name="str",
            replica_name="str",
            api_version="2024-06-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
