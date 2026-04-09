"""GitHub Actions deployment."""

from __future__ import annotations

import os
from pathlib import Path

from rich import print  # type: ignore

from dotflow.cloud.core import Deployer
from dotflow.cloud.github.constants import PYGITHUB_NOT_FOUND, TOKEN_NOT_FOUND
from dotflow.settings import Settings as settings


class ActionsDeployer(Deployer):
    """Deploy dotflow pipeline to GitHub Actions."""

    def __init__(self, token: str = None):
        try:
            from github import Github, GithubException
        except ImportError as err:
            raise SystemExit(PYGITHUB_NOT_FOUND) from err

        self._token = token or os.environ.get("GITHUB_TOKEN")
        if not self._token:
            raise SystemExit(TOKEN_NOT_FOUND)

        self._github = Github(self._token)
        self._GithubException = GithubException
        self._user = self._github.get_user()

    def deploy(self, name: str, **kwargs) -> None:
        """Create repo and push all project files."""
        print(settings.INFO_ALERT, f"Deploying to GitHub Actions '{name}'...")

        repo = self._create_or_get_repo(name)
        self._push_files(repo)

        print(f"  Repository: {repo.html_url}")
        print(f"  Actions: {repo.html_url}/actions")
        print(settings.INFO_ALERT, "Done.")

    def _create_or_get_repo(self, name: str):
        """Create repo or get existing."""
        try:
            repo = self._user.get_repo(name)
            print(f"  Using existing repo '{name}'")
            return repo
        except self._GithubException:
            pass

        print(f"  Creating repo '{name}'...")
        return self._user.create_repo(
            name=name,
            private=True,
            auto_init=False,
        )

    def _push_files(self, repo):
        """Push all project files to the repo."""
        print("  Pushing files...")

        project_dir = Path.cwd()
        tracked = self._get_tracked_files(project_dir)
        count = 0

        for relative in tracked:
            filepath = project_dir / relative

            try:
                content = filepath.read_text()
            except UnicodeDecodeError:
                continue

            self._create_or_update_file(repo, relative, content)
            count += 1

        print(f"  Pushed {count} files")

    def _get_tracked_files(self, project_dir: Path) -> list[str]:
        """Get files that git would track, respecting .gitignore."""
        from git import Repo

        repo = Repo(project_dir)
        tracked = set(repo.git.ls_files("--cached").splitlines())
        untracked = set(
            repo.git.ls_files("--others", "--exclude-standard").splitlines()
        )
        return sorted(tracked | untracked)

    def _create_or_update_file(self, repo, path: str, content: str):
        """Create or update a single file in the repo."""
        try:
            existing = repo.get_contents(path)
            repo.update_file(
                path=path,
                message=f"update {path}",
                content=content,
                sha=existing.sha,
            )
        except self._GithubException:
            repo.create_file(
                path=path,
                message=f"add {path}",
                content=content,
            )
