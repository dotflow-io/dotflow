"""Command cloud module"""

from __future__ import annotations

import json
import re
from pathlib import Path
from subprocess import run

from rich import print  # type: ignore
from rich.console import Console
from rich.table import Table

from dotflow.cli.command import Command
from dotflow.settings import Settings as settings


def _get_template_dir() -> Path | None:
    import tempfile

    target = Path(tempfile.gettempdir()) / "dotflow-template"
    cloud_dir = target / settings.TEMPLATE_CLOUD_DIR

    if cloud_dir.exists():
        run(
            ["git", "-C", str(target), "pull", "--ff-only"],
            capture_output=True,
            text=True,
        )
        return cloud_dir

    try:
        result = run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                settings.TEMPLATE_BRANCH,
                settings.TEMPLATE_REPO,
                str(target),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return cloud_dir
    except Exception as err:
        print(
            settings.ERROR_ALERT,
            f"Failed to clone template repository: {err}",
        )

    return None


def _load_registry(cloud_dir: Path) -> dict | None:
    registry_path = cloud_dir / "registry.json"
    if not registry_path.exists():
        print(settings.ERROR_ALERT, "Registry not found in template.")
        return None

    try:
        return json.loads(registry_path.read_text())
    except Exception as err:
        print(settings.ERROR_ALERT, f"Failed to read registry: {err}")
        return None


def _get_platforms(registry: dict) -> dict | None:
    platforms = registry.get("platforms")
    if not isinstance(platforms, dict):
        print(settings.ERROR_ALERT, "Unexpected registry format.")
        return None

    return platforms


def _read_project_name(pyproject: Path) -> str | None:
    try:
        in_project = False
        for line in pyproject.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                in_project = stripped in ("[project]", "[tool.poetry]")
            if in_project and re.match(r"^name\s*=", stripped):
                return stripped.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        return None
    return None


class CloudGenerateCommand(Command):
    def setup(self):
        platform = self.params.platform

        cloud_dir = _get_template_dir()
        if cloud_dir is None:
            return

        registry = _load_registry(cloud_dir)
        if registry is None:
            return

        platforms = _get_platforms(registry)
        if platforms is None:
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

        project_name = self.params.project
        if not project_name:
            pyproject = Path.cwd() / "pyproject.toml"
            if pyproject.exists():
                project_name = _read_project_name(pyproject)
            if not project_name:
                project_name = Path.cwd().name

        project_name = project_name.replace("_", "-").lower()
        module_name = project_name.replace("-", "_")

        print(
            settings.INFO_ALERT,
            f"Generating {platform_info.get('name', platform)} files"
            f" for '{project_name}'...",
        )

        source_dir = cloud_dir / platform

        for filename in files:
            filepath = (output / filename).resolve()
            try:
                filepath.relative_to(output)
            except ValueError:
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

            source = source_dir / filename
            if not source.exists():
                print(
                    settings.ERROR_ALERT,
                    f"  Skipped (template not found): {filename}",
                )
                continue

            content = source.read_text()
            content = content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{MODULE_NAME}}", module_name)

            filepath.write_text(content)
            print(f"  Created: {filepath}")

        print(settings.INFO_ALERT, "Done.")


class CloudListCommand(Command):
    def setup(self):
        cloud_dir = _get_template_dir()
        if cloud_dir is None:
            return

        registry = _load_registry(cloud_dir)
        if registry is None:
            return

        platforms = _get_platforms(registry)
        if platforms is None:
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
