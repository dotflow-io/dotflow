"""Command cloud module"""

from pathlib import Path

from requests import get
from rich import print  # type: ignore

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

        print("\nAvailable platforms:\n")
        for key, info in registry["platforms"].items():
            files = ", ".join(info["files"])
            print(f"  {key:<15} {info['name']}")
            print(f"  {'':<15} {info['description']}")
            print(f"  {'':<15} Files: {files}\n")
