# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import asyncio

from devtools_testutils import AzureRecordedTestCase

from azure.keyvault.certificates._shared import HttpChallengeCache


class KeyVaultTestCase(AzureRecordedTestCase):
    def get_resource_name(self, name):
        """helper to create resources with a consistent, test-indicative prefix"""
        return super(KeyVaultTestCase, self).get_resource_name("livekvtest{}".format(name))

    async def _poll_until_no_exception(self, fn, expected_exception, max_retries=20, retry_delay=3):
        """polling helper for live tests because some operations take an unpredictable amount of time to complete"""

        for i in range(max_retries):
            try:
                return await fn()
            except expected_exception:
                if i == max_retries - 1:
                    raise
                if self.is_live:
                    await asyncio.sleep(retry_delay)

    async def _poll_until_exception(self, fn, expected_exception, max_retries=20, retry_delay=3):
        """polling helper for live tests because some operations take an unpredictable amount of time to complete"""

        for _ in range(max_retries):
            try:
                await fn()
                if self.is_live:
                    await asyncio.sleep(retry_delay)
            except expected_exception:
                return
        self.fail("expected exception {expected_exception} was not raised")

    def teardown_method(self, method):
        HttpChallengeCache.clear()
        assert len(HttpChallengeCache._cache) == 0
