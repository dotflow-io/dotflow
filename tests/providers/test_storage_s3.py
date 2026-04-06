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
    @mock_aws
    def setUp(self):
        self.conn = boto3.client("s3", region_name=REGION)
        self.conn.create_bucket(Bucket=BUCKET)

    @mock_aws
    def test_storage_s3_instance(self):
        self.conn.create_bucket(Bucket=BUCKET)
        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)

        self.assertEqual(storage.bucket, BUCKET)
        self.assertEqual(storage.prefix, PREFIX)

    @mock_aws
    def test_post(self):
        self.conn.create_bucket(Bucket=BUCKET)
        expected_value = {"foo": "bar"}

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test.json", context=Context(storage=expected_value))

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test.json")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(loads(data[0]), expected_value)

    @mock_aws
    def test_post_many(self):
        self.conn.create_bucket(Bucket=BUCKET)
        expected_one = {"foo": True}
        expected_two = {"foo": False}

        input_value = Context(
            storage=[
                Context(storage=expected_one),
                Context(storage=expected_two),
            ]
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test.json", context=input_value)

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test.json")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(loads(data[0]), expected_one)
        self.assertEqual(loads(data[1]), expected_two)

    @mock_aws
    def test_post_with_existing_key(self):
        self.conn.create_bucket(Bucket=BUCKET)
        expected_one = {"foo": "bar"}
        expected_two = True

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test.json",
            Body=dumps([dumps(expected_one)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        storage.post(key="test.json", context=Context(storage=expected_two))

        obj = self.conn.get_object(Bucket=BUCKET, Key=f"{PREFIX}test.json")
        data = loads(obj["Body"].read().decode("utf-8"))

        self.assertEqual(loads(data[0]), expected_one)
        self.assertEqual(loads(data[1]), expected_two)

    @mock_aws
    def test_get(self):
        self.conn.create_bucket(Bucket=BUCKET)
        expected_value = {"foo": "bar"}

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test.json",
            Body=dumps([dumps(expected_value)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="test.json")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value)

    @mock_aws
    def test_get_many(self):
        self.conn.create_bucket(Bucket=BUCKET)
        expected_one = {"foo": "bar"}
        expected_two = True

        self.conn.put_object(
            Bucket=BUCKET,
            Key=f"{PREFIX}test.json",
            Body=dumps([dumps(expected_one), dumps(expected_two)]),
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="test.json")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage[0].storage, expected_one)
        self.assertEqual(result.storage[1].storage, expected_two)

    @mock_aws
    def test_get_nonexistent_key(self):
        self.conn.create_bucket(Bucket=BUCKET)

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.get(key="nonexistent.json")

        self.assertIsInstance(result, Context)
        self.assertIsNone(result.storage)

    @mock_aws
    def test_key(self):
        self.conn.create_bucket(Bucket=BUCKET)
        workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=workflow_id,
            step=action_step,
        )

        storage = StorageS3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = storage.key(task=task)

        self.assertEqual(result, f"{workflow_id}-0.json")
