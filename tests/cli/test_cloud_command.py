"""Tests for CloudGenerateCommand."""

from types import SimpleNamespace

from dotflow.cli.commands.cloud import CloudGenerateCommand


def _run_generate(platform, output):
    cmd = CloudGenerateCommand.__new__(CloudGenerateCommand)
    cmd.params = SimpleNamespace(
        platform=platform, project="demo", output=str(output)
    )
    cmd.setup()


def test_generate_github_actions_creates_nested_dirs(tmp_path):
    _run_generate("github-actions", tmp_path)

    workflow = tmp_path / ".github" / "workflows" / "dotflow.yml"
    assert workflow.is_file()
    assert "{{PROJECT_NAME}}" not in workflow.read_text()


def test_generate_docker_writes_files(tmp_path):
    _run_generate("docker", tmp_path)

    assert any(tmp_path.iterdir())
