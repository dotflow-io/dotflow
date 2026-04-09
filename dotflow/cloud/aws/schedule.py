"""AWS EventBridge schedule helpers."""

import re
from pathlib import Path

RATE_PATTERN = re.compile(r"^rate\(.+\)$")
CRON_AWS_PATTERN = re.compile(r"^cron\(.+\)$")


class AWSSchedule:
    """AWS EventBridge schedule helpers."""

    @staticmethod
    def convert(expression: str) -> str:
        """Converts a schedule expression to AWS EventBridge format.

        - rate(...) → passed through
        - cron(...) → passed through (assumed valid 6-field AWS cron)
        - 5-field crontab → converted to cron(min hour day-of-month month ? year)
        """
        expression = expression.strip()

        if RATE_PATTERN.match(expression):
            return expression

        if CRON_AWS_PATTERN.match(expression):
            return expression

        return _crontab_to_aws(expression)

    @staticmethod
    def read_from_template(path: Path = Path("template.yaml")) -> str | None:
        """Reads a schedule expression from a SAM template.yaml file."""
        if not path.exists():
            return None
        try:
            import yaml

            data = yaml.safe_load(path.read_text())
            resources = data.get("Resources", {})
            for resource in resources.values():
                events = resource.get("Properties", {}).get("Events", {})
                for event in events.values():
                    if event.get("Type") == "Schedule":
                        schedule = event.get("Properties", {}).get("Schedule")
                        if schedule:
                            return schedule
        except Exception:
            pass
        return None


def _crontab_to_aws(expression: str) -> str:
    """Converts 5-field crontab to 6-field AWS EventBridge cron."""
    parts = expression.split()

    if len(parts) != 5:
        return expression

    minute, hour, dom, month, dow = parts

    if dow != "*" and dom == "*":
        dom = "?"
    else:
        dow = "?"

    return f"cron({minute} {hour} {dom} {month} {dow} *)"
