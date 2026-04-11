"""Alibaba Function Compute Scheduled deployment."""

from __future__ import annotations

from rich import print  # type: ignore

from dotflow.cloud.alibaba.deployers.fc import (
    AliyunFCDeployer,
)
from dotflow.settings import Settings as settings


class AliyunFCScheduledDeployer(AliyunFCDeployer):
    """Deploy dotflow pipeline as Alibaba FC + timer trigger."""

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy FC function with timer trigger."""
        name = self._sanitize_name(name)
        schedule = kwargs.get("schedule")

        print(
            settings.INFO_ALERT,
            f"Deploying to Alibaba FC scheduled '{name}'...",
        )

        image_uri = self._cr.push(name)
        self._create_or_update_function(name, image_uri)

        if schedule:
            self._configure_trigger(name, schedule)

        print(settings.INFO_ALERT, "Done.")

    def _configure_trigger(self, name: str, schedule: str) -> None:
        """Create timer trigger on FC function."""
        from alibabacloud_fc_open20210406 import models

        trigger_name = f"{name}-timer"

        print(
            f"  {settings.STEP_ICON} "
            f"Creating timer trigger '{trigger_name}'..."
        )

        try:
            self._fc.get_trigger(name, trigger_name)
            self._fc.update_trigger(
                name,
                trigger_name,
                models.UpdateTriggerRequest(
                    trigger_config=(
                        models.TimerTriggerConfig(
                            cron_expression=schedule,
                            payload="{}",
                            enable=True,
                        )
                    ),
                ),
            )
        except Exception as err:
            if not (hasattr(err, "status_code") and err.status_code == 404):
                raise
            self._fc.create_trigger(
                name,
                models.CreateTriggerRequest(
                    trigger_name=trigger_name,
                    trigger_type="timer",
                    trigger_config=(
                        models.TimerTriggerConfig(
                            cron_expression=schedule,
                            payload="{}",
                            enable=True,
                        )
                    ),
                ),
            )

        print(f"  {settings.STEP_ICON} Cron: {schedule}")
