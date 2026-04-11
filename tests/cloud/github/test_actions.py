"""Test ActionsDeployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.core import Deployer
from dotflow.cloud.github.deployers.actions import ActionsDeployer


class _GithubException(Exception):
    pass


class TestActionsDeployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(ActionsDeployer, "__init__", return_value=None):
            deployer = ActionsDeployer()
        deployer._github = MagicMock()
        deployer._GithubException = _GithubException
        deployer._user = MagicMock()
        deployer._token = "fake-token"
        return deployer

    def test_instance(self):
        deployer = self._make_deployer()
        self.assertIsInstance(deployer, Deployer)

    def test_create_new_repo(self):
        deployer = self._make_deployer()
        deployer._user.get_repo.side_effect = _GithubException()
        mock_repo = MagicMock()
        deployer._user.create_repo.return_value = mock_repo

        repo = deployer._create_or_get_repo("test")

        deployer._user.create_repo.assert_called_once()
        self.assertEqual(repo, mock_repo)

    def test_use_existing_repo(self):
        deployer = self._make_deployer()
        mock_repo = MagicMock()
        deployer._user.get_repo.return_value = mock_repo

        repo = deployer._create_or_get_repo("test")

        deployer._user.create_repo.assert_not_called()
        self.assertEqual(repo, mock_repo)

    def test_create_file(self):
        deployer = self._make_deployer()
        mock_repo = MagicMock()
        mock_repo.get_contents.side_effect = _GithubException()

        deployer._create_or_update_file(mock_repo, "test.py", "print('hi')")

        mock_repo.create_file.assert_called_once()

    def test_update_existing_file(self):
        deployer = self._make_deployer()
        mock_repo = MagicMock()
        mock_existing = MagicMock()
        mock_existing.sha = "abc123"
        mock_repo.get_contents.return_value = mock_existing

        deployer._create_or_update_file(mock_repo, "test.py", "print('hi')")

        mock_repo.update_file.assert_called_once()

    def test_deploy_creates_repo_and_pushes(self):
        deployer = self._make_deployer()
        mock_repo = MagicMock()
        mock_repo.html_url = "https://github.com/user/test"
        deployer._user.get_repo.return_value = mock_repo
        mock_repo.get_contents.side_effect = _GithubException()

        with patch.object(deployer, "_push_files") as mock_push:
            deployer.deploy("test")

            mock_push.assert_called_once_with(mock_repo)
