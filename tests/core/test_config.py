"""Test Config class"""

import unittest

from dotflow.abc.api import Api
from dotflow.abc.log import Log
from dotflow.abc.notify import Notify
from dotflow.abc.scheduler import Scheduler
from dotflow.abc.storage import Storage
from dotflow.core.config import Config
from dotflow.core.exception import NotCallableObject
from dotflow.providers import (
    LogDefault,
    NotifyDefault,
    SchedulerDefault,
    StorageDefault,
)
from dotflow.providers.api_default import ApiDefault


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = Config()

        self.assertIsInstance(config.storage, Storage)
        self.assertIsInstance(config.notify, Notify)
        self.assertIsInstance(config.log, Log)
        self.assertIsInstance(config.api, Api)
        self.assertIsInstance(config.scheduler, Scheduler)

    def test_default_provider_types(self):
        config = Config()

        self.assertIsInstance(config.storage, StorageDefault)
        self.assertIsInstance(config.notify, NotifyDefault)
        self.assertIsInstance(config.log, LogDefault)
        self.assertIsInstance(config.api, ApiDefault)
        self.assertIsInstance(config.scheduler, SchedulerDefault)

    def test_invalid_storage_raises(self):
        with self.assertRaises(NotCallableObject):
            Config(storage="invalid")

    def test_invalid_notify_raises(self):
        with self.assertRaises(NotCallableObject):
            Config(notify="invalid")

    def test_invalid_log_raises(self):
        with self.assertRaises(NotCallableObject):
            Config(log="invalid")

    def test_invalid_api_raises(self):
        with self.assertRaises(NotCallableObject):
            Config(api="invalid")

    def test_invalid_scheduler_raises(self):
        with self.assertRaises(NotCallableObject):
            Config(scheduler="invalid")

    def test_custom_storage(self):
        storage = StorageDefault()
        config = Config(storage=storage)

        self.assertIs(config.storage, storage)

    def test_custom_scheduler(self):
        scheduler = SchedulerDefault()
        config = Config(scheduler=scheduler)

        self.assertIs(config.scheduler, scheduler)

    def test_default_providers_are_not_shared_between_instances(self):
        config_a = Config()
        config_b = Config()

        self.assertIsNot(
            config_a.storage,
            config_b.storage,
            "Each Config() call must produce a fresh StorageDefault instance",
        )
        self.assertIsNot(
            config_a.notify,
            config_b.notify,
            "Each Config() call must produce a fresh NotifyDefault instance",
        )
