"""Test tools"""

import unittest
from pathlib import Path

from dotflow.utils.tools import read_file, write_file


class TestWriteFile(unittest.TestCase):
    def setUp(self):
        self.file_path = Path("tests", "test_tools.txt")

    def tearDown(self):
        if self.file_path.exists():
            self.file_path.unlink()

    def test_write_mode_creates_file_with_content(self):
        write_file(path=str(self.file_path), content="hello", mode="w")

        with open(self.file_path) as f:
            self.assertIn("hello", f.read())

    def test_append_mode_adds_content(self):
        write_file(path=str(self.file_path), content="first", mode="w")
        write_file(path=str(self.file_path), content="second", mode="a")

        with open(self.file_path) as f:
            content = f.read()

        self.assertIn("first", content)
        self.assertIn("second", content)


class TestReadFile(unittest.TestCase):
    def setUp(self):
        self.file_path = Path("tests", "test_read.txt")

    def tearDown(self):
        if self.file_path.exists():
            self.file_path.unlink()

    def test_returns_none_when_file_does_not_exist(self):
        result = read_file(path=Path("tests", "nonexistent.txt"))

        self.assertIsNone(result)

    def test_returns_parsed_json(self):
        with open(self.file_path, "w") as f:
            f.write('{"foo": "bar"}')

        result = read_file(path=self.file_path)

        self.assertEqual(result, {"foo": "bar"})

    def test_returns_raw_string_when_not_valid_json(self):
        with open(self.file_path, "w") as f:
            f.write("plain text content")

        result = read_file(path=self.file_path)

        self.assertEqual(result, "plain text content")
