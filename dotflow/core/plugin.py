"""Plugins module."""

import sys
import threading

from typing import Union

if sys.version_info >= (3, 10):
    from importlib.metadata import EntryPoint, entry_points
else:
    from importlib_metadata import EntryPoint, entry_points

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

    def __init__(self):
        self._plugins = self._loading_native_plugins()

        if not self._plugins:
            self._loading_external_plugins(
                plugins=[
                    LogsHandler,
                    MetricsHandler,
                    NotifyHandler,
                    StorageHandler
                ]
            )

    def _loading_native_plugins(self):
        plugin_map = {}
        plugins = entry_points(group="dotflow.plugins")

        for plugin in plugins:
            plugin_cls = plugin.load()
            included_plugin = PluginInstance(instance=plugin_cls)

            plugin_map[included_plugin.group] = included_plugin.instance
            setattr(self, plugin.name, included_plugin.instance)

        return plugin_map

    def _loading_external_plugins(self, plugins):
        if isinstance(plugins, list):
            for plugin in plugins:
                current_plugin = PluginInstance(instance=plugin)
                self._plugins[current_plugin.group] = current_plugin.instance
                setattr(self, current_plugin.group, current_plugin.instance)
        else:
            current_plugin = PluginInstance(instance=plugins)
            self._plugins[current_plugin.group] = current_plugin.instance
            setattr(self, current_plugin.group, current_plugin.instance)

        return self

    def handler(self, option: str, value: str, **kwargs):
        callable_group = getattr(self.plugins, option)
        new_callable = getattr(callable_group, value)

        thread = threading.Thread(
            target=new_callable,
            kwargs=kwargs
        )
        thread.start()
