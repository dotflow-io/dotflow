"""Test StorageFile"""

import unittest

from uuid import uuid4
from pathlib import Path
from shutil import rmtree
from json import dumps, loads

from dotflow.core.task import Task
from dotflow.core.context import Context
from dotflow.providers.storage_file import StorageFile

from tests.mocks import action_step


class TestStorageFile(unittest.TestCase):

    def setUp(self):
        self.path = Path("tests")
        self.file_name = "file.json"

    def tearDown(self):
        rmtree(self.path.joinpath("tasks"))

    def test_storage_file_instance(self):
        storage = StorageFile(path=self.path)

        self.assertTrue(storage.path.exists())

    def test_post(self):
        expected_value = {"foo": "bar"}

        storage = StorageFile(path=self.path)
        storage.post(key=self.file_name, context=Context(storage=expected_value))

        self.assertTrue(storage.path.joinpath(self.file_name).exists())

        with open(file=self.path.joinpath("tasks", self.file_name), mode="r") as file:
            result = loads(file.read())

            self.assertEqual(loads(result[0]), expected_value)

    def test_post_many(self):
        expected_value_one = {"foo": True}
        expected_value_two = {"foo": False}

        input_value = Context(
            storage=[
                Context(storage=expected_value_one),
                Context(storage=expected_value_two),
            ]
        )

        storage = StorageFile(path=self.path)
        storage.post(key=self.file_name, context=input_value)

        self.assertTrue(storage.path.joinpath(self.file_name).exists())

        with open(file=self.path.joinpath("tasks", self.file_name), mode="r") as file:
            result = loads(file.read())

            self.assertEqual(loads(result[0]), expected_value_one)
            self.assertEqual(loads(result[1]), expected_value_two)

    def test_post_with_existing_file(self):
        expected_value_one = {"foo": "bar"}
        expected_value_two = True

        self.path.joinpath("tasks").mkdir()

        with open(file=self.path.joinpath("tasks", self.file_name), mode="w") as file:
            file.write(dumps([dumps(expected_value_one)]))

        storage = StorageFile(path=self.path)
        storage.post(key=self.file_name, context=Context(storage=expected_value_two))

        self.assertTrue(storage.path.joinpath(self.file_name).exists())

        with open(file=self.path.joinpath("tasks", self.file_name), mode="r") as file:
            result = loads(file.read())

            self.assertEqual(loads(result[0]), expected_value_one)
            self.assertEqual(loads(result[1]), expected_value_two)

    def test_get(self):
        expected_value = [{"foo": "bar"}]
        self.path.joinpath("tasks").mkdir()

        with open(file=self.path.joinpath("tasks", self.file_name), mode="w") as file:
            file.write(dumps(expected_value))

        storage = StorageFile(path=self.path)
        result = storage.get(key=self.file_name)

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value[0])

    def test_get_many(self):
        expected_value_one = {"foo": "bar"}
        expected_value_two = True

        self.path.joinpath("tasks").mkdir()

        with open(file=self.path.joinpath("tasks", self.file_name), mode="w") as file:
            file.write(dumps([expected_value_one, expected_value_two]))

        storage = StorageFile(path=self.path)
        result = storage.get(key=self.file_name)

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage[0].storage, expected_value_one)
        self.assertEqual(result.storage[1].storage, expected_value_two)

    def test_key(self):
        workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=workflow_id,
            step=action_step,
        )

        storage = StorageFile(path=self.path)
        result = storage.key(task=task)

        self.assertEqual(result, f"{workflow_id}-0.json")
