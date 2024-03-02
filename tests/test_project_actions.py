import os
import shutil
from pathlib import Path

from typer.testing import CliRunner

from jampy_cli import app
from jampy_cli.common_utils import get_cwd

runner = CliRunner()


def assert_target_not_exists(target: Path):
    assert target.exists() is False


def assert_target_exists(target: Path):
    assert target.exists() is True


def test_create_project():
    def assert_ok(project_dir: Path):
        assert result.exit_code == 0
        assert_target_exists(project_dir)
        assert_target_exists(project_dir / '.gitignore')
        shutil.rmtree(project_dir)

    def assert_misuse():
        assert result.exit_code == 2
        assert 'usage' in result.stdout.lower()

    def assert_exit_if_duplicated(project_dir: Path):
        assert result.exit_code == 0
        assert 'already exists' in result.stdout.lower()
        shutil.rmtree(project_dir)

    name = "temp_project"
    project_dir = Path(f"{get_cwd()}/{name}")
    if project_dir.exists():
        shutil.rmtree(project_dir)

    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project", "create", "-p", name])
    assert_ok(project_dir)

    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project", "c", "--path", name])
    assert_ok(project_dir)

    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project", "c", name])
    assert_misuse()

    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project"])
    assert_misuse()

    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project", "create", "-p", name])
    assert_target_exists(project_dir)
    result = runner.invoke(app, ["project", "create", "-p", name])
    assert_exit_if_duplicated(project_dir)

    sub_name = 'sub_temp_project'
    sub_project_dir = project_dir.joinpath(sub_name)
    assert_target_not_exists(project_dir)
    assert_target_not_exists(sub_project_dir)
    result = runner.invoke(app, ["project", "create", "-p", f"{name}/{sub_name}"])
    assert_ok(sub_project_dir)
    shutil.rmtree(project_dir)


def test_sync_settings():
    def assert_ok(project_dir: Path):
        assert result.exit_code == 0
        setting_dir = project_dir.joinpath('.vscode')
        assert_target_exists(setting_dir.joinpath('settings.json'))
        backups = list(setting_dir.glob('settings_back*'))
        assert len(backups) == 1
        os.remove(backups[0])

    name = "temp_project"
    project_dir = Path(f"{get_cwd()}/{name}")
    if project_dir.exists():
        shutil.rmtree(project_dir)
    result = runner.invoke(app, ["project", "sync-settings"])
    assert_ok(project_dir.parent)
