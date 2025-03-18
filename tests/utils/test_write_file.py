"""Test utils"""

import unittest

from pathlib import Path

from dotflow.utils import write_file

from tests.mocks import simple_step


class TestWriteFile(unittest.TestCase):

    def setUp(self):
        self.file_path = Path("tests", "test.txt")

    def tearDown(self):
        self.file_path.unlink()

    def test_write_file_with_str(self):
        expected_value = '"str"'

        write_file(path=self.file_path, content="str")

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_int(self):
        expected_value = '1'

        write_file(path=self.file_path, content=1)

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_float(self):
        expected_value = '1.0'

        write_file(path=self.file_path, content=1.0)

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_complex(self):
        expected_value = '(3+5j)'

        write_file(path=self.file_path, content=complex(3, 5))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_dict(self):
        expected_value = '{}'
        write_file(path=self.file_path, content={})

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_list(self):
        expected_value = '[]'
        write_file(path=self.file_path, content=[])

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_tuple(self):
        expected_value = '[1, 2, 3]'
        write_file(path=self.file_path, content=(1, 2, 3))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_set(self):
        expected_value = '{1, 2, 3}'
        write_file(path=self.file_path, content={1, 2, 3})

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_frozenset(self):
        expected_value = 'frozenset({1, 2, 3})'
        write_file(path=self.file_path, content=frozenset({1, 2, 3}))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_range(self):
        expected_value = 'range(0, 5)'
        write_file(path=self.file_path, content=range(5))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_func(self):
        expected_value = 'function simple_step'
        write_file(path=self.file_path, content=simple_step)

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read().find(expected_value), 1)

    def test_write_file_with_bool(self):
        expected_value = 'true'
        write_file(path=self.file_path, content=True)

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_none(self):
        expected_value = 'null'
        write_file(path=self.file_path, content=None)

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_bytes(self):
        expected_value = "b'Hello'"
        write_file(path=self.file_path, content=b"Hello")

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_bytearray(self):
        expected_value = "bytearray(b'\\x00\\x00\\x00\\x00\\x00')"
        write_file(path=self.file_path, content=bytearray(5))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read(), expected_value)

    def test_write_file_with_memoryview(self):
        expected_value = "memory"
        write_file(path=self.file_path, content=memoryview(bytes(5)))

        with open(self.file_path, mode="r") as file:
            self.assertEqual(file.read().find(expected_value), 1)
