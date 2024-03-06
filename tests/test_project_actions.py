import shutil
from pathlib import Path

from inflection import underscore
from jampy_util.path import get_absolute_cwd_path
from typer.testing import CliRunner

from jampy_cli import app

runner = CliRunner()


def assert_target_not_exists(target: Path):
    assert target.exists() is False


def assert_target_exists(target: Path):
    assert target.exists() is True


# TODO: optimization with fixture
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

    name = "temp-project"
    project_dir = Path(f"{get_absolute_cwd_path()}/{underscore(name)}")
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

    name = '../temp-project'
    project_dir = Path(
        f"{get_absolute_cwd_path().parent}/{underscore(Path(name).name)}"
    )
    assert_target_not_exists(project_dir)
    result = runner.invoke(app, ["project", "create", "-p", name])
    assert_ok(project_dir)

    parent_name, name = 'temp-dir', 'temp-project'
    project_dir = Path(
        f"{get_absolute_cwd_path()}/{parent_name}/{underscore(name)}"
    )
    assert_target_not_exists(Path(f"{get_absolute_cwd_path()}/{parent_name}"))
    assert_target_not_exists(project_dir)
    result = runner.invoke(
        app, ["project", "create", "-p", f"{parent_name}/{name}"]
    )
    assert_ok(project_dir)
    shutil.rmtree(Path(f"{get_absolute_cwd_path()}/{parent_name}"))

    parent_name, name = 'temp-dir', 'temp-project'
    parent_dir = Path(f"{get_absolute_cwd_path()}/{parent_name}")
    project_dir = Path(f"{parent_dir}/{underscore(name)}")
    if parent_dir.exists():
        shutil.rmtree(parent_dir)
    assert_target_not_exists(parent_dir)
    result = runner.invoke(
        app, ["project", "create", "-p", f"{parent_name}/{name}"]
    )
    assert_ok(project_dir)
    shutil.rmtree(parent_dir)


def test_sync_settings():
    def assert_ok(project_dir: Path):
        assert result.exit_code == 0
        setting_dir = project_dir.joinpath('.vscode')
        assert_target_exists(setting_dir.joinpath('settings.json'))
        backups = list(setting_dir.glob('settings_back*'))
        assert len(backups) == 1
        shutil.move(backups[0], setting_dir.joinpath('settings.json'))

    name = "temp_project"
    project_dir = Path(f"{get_absolute_cwd_path()}/{name}")
    if project_dir.exists():
        shutil.rmtree(project_dir)
    result = runner.invoke(app, ["project", "sync-settings"])
    assert_ok(project_dir.parent)
