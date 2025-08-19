"""Test of config"""

import unittest

from dotflow.core.config import Config, ConfigInstance
from dotflow.abc.storage import Storage
from dotflow.abc.notify import Notify
from dotflow.abc.logs import Logs


class TestConfigInstance(unittest.TestCase):

    def setUp(self):
        self.instance = ConfigInstance()

    def test_instantiating_config_instance_class(self):
        self.assertIsNone(self.instance._storage)
        self.assertIsNone(self.instance._notify)
        self.assertIsNone(self.instance._logs)


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.index = 0

    def test_instantiating_config_class(self):
        self.assertIsInstance(self.config.storage, Storage)
        self.assertIsInstance(self.config.notify, Notify)
        self.assertIsInstance(self.config.logs, list)
        self.assertIsInstance(self.config.logs[self.index], Logs)

    def test_config_storage_object(self):
        self.assertIsNotNone(self.config.storage)
        self.assertFalse(callable(self.config.storage))

    def test_config_notify_object(self):
        self.assertIsNotNone(self.config.notify)
        self.assertFalse(callable(self.config.notify))

    def test_config_logs_object(self):
        self.assertIsNotNone(self.config.logs)
        self.assertFalse(callable(self.config.logs[self.index]))
