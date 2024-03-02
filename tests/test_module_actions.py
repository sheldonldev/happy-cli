# import os
# import shutil
# from pathlib import Path

# from typer.testing import CliRunner

# from jampy_cli import app

# runner = CliRunner()


# def test_create_module():
#     def assert_ok_and_remove():
#         assert result.exit_code == 0
#         assert Path(f"{os.path.abspath(os.getcwd())}/{name}").exists() is True
#         assert Path(f"{os.path.abspath(os.getcwd())}/{name}/.gitignore").exists() is True
#         shutil.rmtree(module_dir)

#     def assert_misuse():
#         assert result.exit_code == 2
#         assert 'usage' in result.stdout.lower()

#     def assert_exists_if_duplicated():
#         assert result.exit_code == 0
#         assert 'already exists' in result.stdout.lower()
#         shutil.rmtree(module_dir)

#     name = "temp_module"
#     module_dir = Path(f"{os.path.abspath(os.getcwd())}/{name}")
#     if module_dir.exists():
#         shutil.rmtree(module_dir)

#     result = runner.invoke(app, ["module", "create", "-p", name])
#     assert_ok_and_remove()

#     result = runner.invoke(app, ["module", "c", "--path", name])
#     assert_ok_and_remove()

#     result = runner.invoke(app, ["module", "c", name])
#     assert_misuse()

#     result = runner.invoke(app, ["module"])
#     assert_misuse()

#     result = runner.invoke(app, ["module", "create", "-p", name])
#     result = runner.invoke(app, ["module", "create", "-p", name])
#     assert_exists_if_duplicated()

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

    name = "temp_module"
    module_dir = Path(f"{get_cwd()}/{name}")
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

    sub_name = 'sub_temp_module'
    sub_module_dir = module_dir.joinpath(sub_name)
    assert_target_not_exists(module_dir)
    assert_target_not_exists(sub_module_dir)
    result = runner.invoke(app, ["module", "create", "-p", f"{name}/{sub_name}"])
    assert_ok(sub_module_dir)
    shutil.rmtree(module_dir)
