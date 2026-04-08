"""Test S3 service."""

import unittest

import boto3
from moto import mock_aws

from dotflow.cloud.aws.services.s3 import S3
from dotflow.cloud.core import ObjectStorage

BUCKET = "test-bucket"
PREFIX = "dotflow/"
REGION = "us-east-1"


class TestS3(unittest.TestCase):
    def setUp(self):
        self.mock = mock_aws()
        self.mock.start()
        boto3.client("s3", region_name=REGION).create_bucket(Bucket=BUCKET)

    def tearDown(self):
        self.mock.stop()

    def test_instance(self):
        s3 = S3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        self.assertIsInstance(s3, ObjectStorage)

    def test_write_and_read(self):
        s3 = S3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        s3.write("key1", [{"a": 1}])
        result = s3.read("key1")
        self.assertEqual(result, [{"a": 1}])

    def test_read_nonexistent(self):
        s3 = S3(bucket=BUCKET, prefix=PREFIX, region=REGION)
        result = s3.read("missing")
        self.assertEqual(result, [])
