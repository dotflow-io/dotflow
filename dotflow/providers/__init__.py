"""Providers __init__ module."""

from dotflow.providers.log_default import LogDefault
from dotflow.providers.notify_default import NotifyDefault
from dotflow.providers.notify_discord import NotifyDiscord
from dotflow.providers.notify_telegram import NotifyTelegram
from dotflow.providers.scheduler_default import SchedulerDefault
from dotflow.providers.storage_default import StorageDefault
from dotflow.providers.storage_file import StorageFile

__all__ = [
    "LogDefault",
    "LogOpenTelemetry",
    "NotifyDefault",
    "NotifyDiscord",
    "NotifyTelegram",
    "SchedulerCron",
    "SchedulerDefault",
    "StorageDefault",
    "StorageFile",
    "StorageS3",
    "StorageGCS",
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

    if name == "LogOpenTelemetry":
        from dotflow.providers.log_opentelemetry import LogOpenTelemetry

        return LogOpenTelemetry

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
