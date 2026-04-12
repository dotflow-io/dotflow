"""Providers __init__ module."""

from dotflow.providers.log_default import LogDefault
from dotflow.providers.metrics_default import MetricsDefault
from dotflow.providers.notify_default import NotifyDefault
from dotflow.providers.notify_discord import NotifyDiscord
from dotflow.providers.notify_telegram import NotifyTelegram
from dotflow.providers.scheduler_default import SchedulerDefault
from dotflow.providers.server_api import ServerAPI
from dotflow.providers.server_default import ServerDefault
from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.storage_file import StorageFile
from dotflow.providers.tracer_default import TracerDefault

__all__ = [
    "LogDefault",
    "LogOpenTelemetry",
    "LogSentry",
    "NotifyDefault",
    "NotifyDiscord",
    "NotifyTelegram",
    "SchedulerCron",
    "SchedulerDefault",
    "ServerAPI",
    "ServerDefault",
    "StorageDefault",
    "StorageFile",
    "StorageS3",
    "StorageGCS",
    "MetricsDefault",
    "MetricsOpenTelemetry",
    "TracerDefault",
    "TracerOpenTelemetry",
    "TracerSentry",
]


def __getattr__(name):
    if name == "StorageS3":
        from dotflow.providers.storage_s3 import StorageS3

        return StorageS3

    if name == "StorageGCS":
        from dotflow.providers.storage_gcs import StorageGCS

        return StorageGCS

    if name == "SchedulerCron":
        from dotflow.providers.scheduler_cron import SchedulerCron

        return SchedulerCron

    if name == "TracerOpenTelemetry":
        from dotflow.providers.tracer_opentelemetry import TracerOpenTelemetry

        return TracerOpenTelemetry

    if name == "MetricsOpenTelemetry":
        from dotflow.providers.metrics_opentelemetry import (
            MetricsOpenTelemetry,
        )

        return MetricsOpenTelemetry

    if name == "LogOpenTelemetry":
        from dotflow.providers.log_opentelemetry import LogOpenTelemetry

        return LogOpenTelemetry

    if name == "LogSentry":
        from dotflow.providers.log_sentry import LogSentry

        return LogSentry

    if name == "TracerSentry":
        from dotflow.providers.tracer_sentry import TracerSentry

        return TracerSentry

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
