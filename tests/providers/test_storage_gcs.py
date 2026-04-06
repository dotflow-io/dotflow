"""Test StorageGCS"""

import unittest
from json import dumps, loads
from unittest.mock import MagicMock, patch
from uuid import uuid4

from dotflow.core.context import Context
from dotflow.core.task import Task
from tests.mocks import action_step

BUCKET = "test-dotflow-bucket"
PREFIX = "dotflow/"
PROJECT = "test-project"


class TestStorageGCS(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_bucket = MagicMock()
        self.mock_client.bucket.return_value = self.mock_bucket

        patcher = patch(
            "dotflow.providers.storage_gcs.StorageGCS.__init__",
            return_value=None,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        from dotflow.providers.storage_gcs import StorageGCS

        self.storage = StorageGCS()
        self.storage.client = self.mock_client
        self.storage.bucket_obj = self.mock_bucket
        self.storage.prefix = PREFIX
        self.storage._not_found = Exception

    def test_storage_gcs_instance(self):
        self.assertEqual(self.storage.prefix, PREFIX)

    def test_post(self):
        expected_value = {"foo": "bar"}
        mock_blob = MagicMock()
        self.mock_bucket.blob.return_value = mock_blob

        self.storage.post(key="test", context=Context(storage=expected_value))

        self.mock_bucket.blob.assert_called_once_with(f"{PREFIX}test")
        mock_blob.upload_from_string.assert_called_once()
        uploaded = mock_blob.upload_from_string.call_args
        data = loads(uploaded[0][0])
        self.assertEqual(loads(data[0]), expected_value)

    def test_post_many(self):
        expected_one = {"foo": True}
        expected_two = {"foo": False}
        mock_blob = MagicMock()
        self.mock_bucket.blob.return_value = mock_blob

        input_value = Context(
            storage=[
                Context(storage=expected_one),
                Context(storage=expected_two),
            ]
        )

        self.storage.post(key="test", context=input_value)

        uploaded = mock_blob.upload_from_string.call_args
        data = loads(uploaded[0][0])
        self.assertEqual(loads(data[0]), expected_one)
        self.assertEqual(loads(data[1]), expected_two)

    def test_post_overwrites_existing_key(self):
        new_value = {"foo": "baz"}
        mock_blob = MagicMock()
        self.mock_bucket.blob.return_value = mock_blob

        self.storage.post(key="test", context=Context(storage=new_value))

        uploaded = mock_blob.upload_from_string.call_args
        data = loads(uploaded[0][0])
        self.assertEqual(len(data), 1)
        self.assertEqual(loads(data[0]), new_value)

    def test_get(self):
        expected_value = {"foo": "bar"}
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_text.return_value = dumps(
            [dumps(expected_value)]
        )
        self.mock_bucket.blob.return_value = mock_blob

        result = self.storage.get(key="test")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value)

    def test_get_many(self):
        expected_one = {"foo": "bar"}
        expected_two = True
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_text.return_value = dumps(
            [dumps(expected_one), dumps(expected_two)]
        )
        self.mock_bucket.blob.return_value = mock_blob

        result = self.storage.get(key="test")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage[0].storage, expected_one)
        self.assertEqual(result.storage[1].storage, expected_two)

    def test_get_nonexistent_key(self):
        mock_blob = MagicMock()
        mock_blob.download_as_text.side_effect = Exception("NotFound")
        self.mock_bucket.blob.return_value = mock_blob

        result = self.storage.get(key="nonexistent")

        self.assertIsInstance(result, Context)
        self.assertIsNone(result.storage)

    def test_key(self):
        workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=workflow_id,
            step=action_step,
        )

        result = self.storage.key(task=task)

        self.assertEqual(result, f"{workflow_id}-0")
