"""Plugins module."""

import sys

import threading

from typing import Union

from importlib.metadata import EntryPoint, entry_points

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)

from dotflow.abc.logs import Logs
from dotflow.abc.metrics import Metrics
from dotflow.abc.notify import Notify
from dotflow.abc.storage import Storage

from dotflow.plugins.logs import LogsHandler
from dotflow.plugins.metrics import MetricsHandler
from dotflow.plugins.notify import NotifyHandler
from dotflow.plugins.storage import StorageHandler


class PluginInstance(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    instance: Union[Logs, Metrics, Notify, Storage]
    group: str = Field(default=None)

    @field_validator('instance', mode='before')
    @classmethod
    def validate_x(cls, value):
        if callable(value):
            value = value()
        return value

    @model_validator(mode='after')
    def check(self):
        self.group = self.instance.group
        return self


class Plugin:

    def __init__(self) -> None:
        self._plugins = {}
        self._loading_native_plugins()

        if not self._plugins:
            self._loading_external_plugins(
                plugins=[
                    LogsHandler,
                    MetricsHandler,
                    NotifyHandler,
                    StorageHandler
                ]
            )

    def _include(self, plugin_object) -> None:
        plugin = PluginInstance(instance=plugin_object)
        self._plugins[plugin.group] = plugin.instance
        setattr(self, plugin.group, plugin.instance)

    def _loading_native_plugins(self) -> dict[str, EntryPoint]:
        plugins = []
        groups = "dotflow.plugins"

        if sys.version_info >= (3, 10):
            plugins = entry_points(group=groups)
        else:
            plugins = entry_points().get(groups, [])

        for plugin in plugins:
            plugin_object = plugin.load()
            self._include(plugin_object=plugin_object)

        return self._plugins

    def _loading_external_plugins(self, plugins) -> dict[str, EntryPoint]:
        if isinstance(plugins, list):
            for plugin in plugins:
                self._include(plugin_object=plugin)
        else:
            self._include(plugin_object=plugins)

        return self._plugins

    def handler(self, option: str, value: str, **kwargs) -> None:
        callable_group = getattr(self._plugins, option)
        new_callable = getattr(callable_group, value)

        thread = threading.Thread(
            target=new_callable,
            kwargs=kwargs
        )
        thread.start()
