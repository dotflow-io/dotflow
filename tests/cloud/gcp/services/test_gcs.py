"""Test GCS service."""

import sys
import unittest
from json import dumps
from unittest.mock import MagicMock, patch

from dotflow.cloud.core import ObjectStorage

mock_gcloud = MagicMock()
sys.modules["google"] = MagicMock()
sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.storage"] = mock_gcloud
sys.modules["google.api_core"] = MagicMock()
sys.modules["google.api_core.exceptions"] = MagicMock()

from dotflow.cloud.gcp.services.gcs import GCS  # noqa: E402, I001


class TestGCS(unittest.TestCase):
    def setUp(self):
        with patch.object(GCS, "__init__", return_value=None):
            self.gcs = GCS()
        self.mock_bucket = MagicMock()
        self.gcs._bucket = self.mock_bucket
        self.gcs._not_found = Exception
        self.gcs.prefix = "dotflow/"

    def test_instance(self):
        self.assertIsInstance(self.gcs, ObjectStorage)

    def test_write(self):
        blob = MagicMock()
        self.mock_bucket.blob.return_value = blob

        self.gcs.write("key1", [{"a": 1}])

        blob.upload_from_string.assert_called_once()

    def test_read(self):
        blob = MagicMock()
        blob.download_as_text.return_value = dumps([{"a": 1}])
        self.mock_bucket.blob.return_value = blob

        result = self.gcs.read("key1")

        self.assertEqual(result, [{"a": 1}])

    def test_read_nonexistent(self):
        blob = MagicMock()
        blob.download_as_text.side_effect = Exception("not found")
        self.mock_bucket.blob.return_value = blob

        result = self.gcs.read("missing")

        self.assertEqual(result, [])
