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


def test_create_module():
    def assert_ok(module_dir: Path):
        assert result.exit_code == 0
        assert_target_exists(module_dir)
        assert_target_exists(module_dir / '.gitignore')
        shutil.rmtree(module_dir)

    def assert_misuse():
        assert result.exit_code == 2
        assert 'usage' in result.stdout.lower()

    def assert_exit_if_duplicated(module_dir: Path):
        assert result.exit_code == 0
        assert 'already exists' in result.stdout.lower()
        shutil.rmtree(module_dir)

    name = "temp-module"
    module_dir = Path(f"{get_absolute_cwd_path()}/{underscore(name)}")
    if module_dir.exists():
        shutil.rmtree(module_dir)

    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module", "create", "-p", name])
    assert_ok(module_dir)

    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module", "c", "--path", name])
    assert_ok(module_dir)

    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module", "c", name])
    assert_misuse()

    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module"])
    assert_misuse()

    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module", "create", "-p", name])
    assert_target_exists(module_dir)
    result = runner.invoke(app, ["module", "create", "-p", name])
    assert_exit_if_duplicated(module_dir)

    name = '../temp-module'
    module_dir = Path(f"{get_absolute_cwd_path().parent}/{underscore(Path(name).name)}")
    if module_dir.exists():
        shutil.rmtree(module_dir)
    assert_target_not_exists(module_dir)
    result = runner.invoke(app, ["module", "create", "-p", name])
    assert_ok(module_dir)

    parent_name, name = 'temp-dir', 'temp-module'
    parent_dir = Path(f"{get_absolute_cwd_path()}/{parent_name}")
    module_dir = Path(f"{parent_dir}/{underscore(name)}")
    if parent_dir.exists():
        shutil.rmtree(parent_dir)
    assert_target_not_exists(parent_dir)
    result = runner.invoke(app, ["module", "create", "-p", f"{parent_name}/{name}"])
    assert_ok(module_dir)
    shutil.rmtree(parent_dir)
