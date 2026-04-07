"""Command cloud module"""

import re
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

        platforms = registry.get("platforms")
        if not isinstance(platforms, dict):
            print(settings.ERROR_ALERT, "Unexpected registry format.")
            return

        if platform not in platforms:
            available = ", ".join(sorted(platforms.keys()))
            print(
                settings.ERROR_ALERT,
                f"Unknown platform '{platform}'. Available: {available}",
            )
            return

        platform_info = platforms[platform]
        files = platform_info.get("files", [])
        output = Path(self.params.output).resolve()
        output.mkdir(parents=True, exist_ok=True)

        project_name, module_name = self._detect_project()

        if self.params.project:
            project_name = self.params.project
            module_name = project_name.replace("-", "_")

        print(
            settings.INFO_ALERT,
            f"Generating {platform_info.get('name', platform)} files"
            f" for '{project_name}'...",
        )

        for filename in files:
            filepath = (output / filename).resolve()
            if not str(filepath).startswith(str(output)):
                print(
                    settings.ERROR_ALERT,
                    f"  Skipped (unsafe filename): {filename}",
                )
                continue

            if filepath.exists():
                print(
                    settings.WARNING_ALERT,
                    f"  Skipped (already exists): {filepath}",
                )
                continue

            content = self._fetch_file(platform, filename)
            if content is None:
                continue

            content = content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{MODULE_NAME}}", module_name)

            filepath.write_text(content)
            print(f"  Created: {filepath}")

        print(settings.INFO_ALERT, "Done.")

    def _detect_project(self):
        path = Path.cwd()
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            name = self._read_project_name(pyproject)
            if name:
                return name, name.replace("-", "_")

        for child in path.iterdir():
            if child.is_dir():
                pyproject = child / "pyproject.toml"
                if pyproject.exists():
                    name = self._read_project_name(pyproject)
                    if name:
                        return name, name.replace("-", "_")

        name = Path.cwd().name
        return name, name.replace("-", "_")

    def _read_project_name(self, pyproject: Path):
        try:
            in_project = False
            for line in pyproject.read_text().splitlines():
                stripped = line.strip()
                if stripped.startswith("["):
                    in_project = stripped in ("[project]", "[tool.poetry]")
                if in_project and re.match(r"^name\s*=", stripped):
                    return (
                        stripped.split("=", 1)[1].strip().strip('"').strip("'")
                    )
        except Exception:
            pass
        return None

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

        platforms = registry.get("platforms")
        if not isinstance(platforms, dict):
            print(settings.ERROR_ALERT, "Unexpected registry format.")
            return

        table = Table(title="Available Platforms")
        table.add_column("Platform", style="bold cyan")
        table.add_column("Name", style="bold")
        table.add_column("Description")

        for key, info in platforms.items():
            table.add_row(
                key,
                info.get("name", ""),
                info.get("description", ""),
            )

        Console().print(table)
