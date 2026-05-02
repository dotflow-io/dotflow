"""StorageDefault contract suite."""

import unittest

from dotflow.providers.storage_default import StorageDefault
from dotflow.testing.storage_contract import StorageContract


class TestStorageDefaultContract(StorageContract, unittest.TestCase):
    def make_storage(self):
        return StorageDefault()
