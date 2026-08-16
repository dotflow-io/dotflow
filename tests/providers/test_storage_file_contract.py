"""StorageFile contract suite."""

import tempfile
import unittest
from pathlib import Path
from shutil import rmtree

from dotflow.providers.storage_file import StorageFile
from dotflow.testing.storage_contract import StorageContract


class TestStorageFileContract(StorageContract, unittest.TestCase):
    def make_storage(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="dotflow-storage-"))

        return StorageFile(path=self._tmp)

    def tearDown(self):
        rmtree(self._tmp, ignore_errors=True)
