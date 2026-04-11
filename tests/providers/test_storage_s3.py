"""Test StorageS3"""

import unittest
from json import dumps, loads
from uuid import uuid4

import boto3
from moto import mock_aws

from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.providers.storage_s3 import StorageS3
from tests.mocks import action_step

BUCKET = "test-dotflow-bucket"
PREFIX = "dotflow/"
REGION = "us-east-1"


class TestStorageS3(unittest.TestCase):
    def setUp(self):
        self.mock = mock_aws()
        self.mock.start()
        self.conn = boto3.client("s3", region_name=REGION)
        self.conn.create_bucket(Bucket=BUCKET)

    def tearDown(self):
        self.mock.stop()

    def test_storage_s3_instance(self):
        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)

        self.assertEqual(storage._s3.bucket, BUCKET)
        self.assertEqual(storage._s3.prefix, PREFIX)

    def test_post(self):
        expected_value = {"foo": "bar"}

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test", context=Context(storage=expected_value))

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(loads(data[0]), expected_value)

    def test_post_many(self):
        expected_one = {"foo": True}
        expected_two = {"foo": False}

        input_value = Context(
            storage=[
                Context(storage=expected_one),
                Context(storage=expected_two),
            ]
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test", context=input_value)

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(loads(data[0]), expected_one)
        self.assertEqual(loads(data[1]), expected_two)

    def test_post_overwrites_existing_key(self):
        old_value = {"foo": "bar"}
        new_value = {"foo": "baz"}

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test",
            Body=dumps([dumps(old_value)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test", context=Context(storage=new_value))

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(len(data), 1)
        self.assertEqual(loads(data[0]), new_value)

    def test_get(self):
        expected_value = {"foo": "bar"}

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test",
            Body=dumps([dumps(expected_value)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="test")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value)

    def test_get_many(self):
        expected_one = {"foo": "bar"}
        expected_two = True

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test",
            Body=dumps([dumps(expected_one), dumps(expected_two)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="test")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage[0].storage, expected_one)
        self.assertEqual(result.storage[1].storage, expected_two)

    def test_get_nonexistent_key(self):
        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="nonexistent")

        self.assertIsInstance(result, Context)
        self.assertIsNone(result.storage)

    def test_key(self):
        workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=workflow_id,
            step=action_step,
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.key(task=task)

        self.assertEqual(result, f"{workflow_id}-0")
