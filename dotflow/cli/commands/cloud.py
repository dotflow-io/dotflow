"""Command cloud module"""

from pathlib import Path

from requests import get
from rich import print  # type: ignore
from rich.console import Console
from rich.table import Table

from dotflow.cli.command import Command
from dotflow.settings import Settings as settings

TEMPLATE_BASE_URL = (
    "https://raw.githubusercontent.com/dotflow-io/template/master/cloud"
)


class CloudGenerateCommand(Command):
    def setup(self):
        platform = self.params.platform

        registry = self._fetch_registry()
        if registry is None:
            return

        if platform not in registry["platforms"]:
            available = ", ".join(sorted(registry["platforms"].keys()))
            print(
                settings.ERROR_ALERT,
                f"Unknown platform '{platform}'. Available: {available}",
            )
            return

        platform_info = registry["platforms"][platform]
        files = platform_info["files"]
        output = Path(self.params.output)
        output.mkdir(parents=True, exist_ok=True)

        project_name = self.params.project or Path.cwd().name
        module_name = project_name.replace("-", "_")

        print(
            settings.INFO_ALERT,
            f"Generating {platform_info['name']} files for '{project_name}'...",
        )

        for filename in files:
            content = self._fetch_file(platform, filename)
            if content is None:
                continue

            content = content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{MODULE_NAME}}", module_name)

            filepath = output / filename
            filepath.write_text(content)
            print(f"  Created: {filepath}")

        print(settings.INFO_ALERT, "Done.")

    def _fetch_registry(self):
        try:
            response = get(f"{TEMPLATE_BASE_URL}/registry.json", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(
                settings.ERROR_ALERT,
                f"Failed to fetch cloud registry: {err}",
            )
            return None

    def _fetch_file(self, platform, filename):
        url = f"{TEMPLATE_BASE_URL}/{platform}/{filename}"
        try:
            response = get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as err:
            print(
                settings.ERROR_ALERT,
                f"Failed to fetch {filename}: {err}",
            )
            return None


class CloudListCommand(Command):
    def setup(self):
        try:
            response = get(f"{TEMPLATE_BASE_URL}/registry.json", timeout=10)
            response.raise_for_status()
            registry = response.json()
        except Exception as err:
            print(
                settings.ERROR_ALERT,
                f"Failed to fetch cloud registry: {err}",
            )
            return

        table = Table(title="Available Platforms")
        table.add_column("Platform", style="bold cyan")
        table.add_column("Name", style="bold")
        table.add_column("Description")

        for key, info in registry["platforms"].items():
            table.add_row(key, info["name"], info["description"])

        Console().print(table)
