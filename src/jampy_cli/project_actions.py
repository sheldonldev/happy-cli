import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from util_common.datetime import format_now
from util_common.path import get_absolute_cwd_path, normalize_path

from ._cfg import STUBS_ROOT
from .notifier import Notifier


def modify_toml(toml_path, project_name):
    toml_str = toml_path.read_text()
    toml_cfg = toml.loads(toml_str)
    toml_cfg["project"]["name"] = project_name
    toml_cfg["project"]["scripts"] = {"run": f"{project_name}.main:main"}
    toml_cfg["tool"]["setuptools"]["packages"]["find"]["include"] = [f"{project_name}*"]
    toml_path.write_text(toml.dumps(toml_cfg))


def modify_cfg(code_path, project_name):
    code_str = code_path.read_text()
    code_lines = code_str.splitlines()
    for i, line in enumerate(code_lines):
        if line.startswith("APP_NAME"):
            code_lines[i] = f'APP_NAME = "{project_name}"'
    code_path.write_text('\n'.join(code_lines) + '\n')


def _replace_import(code_path: Path, project_name):
    code_str = code_path.read_text()
    code_lines = code_str.splitlines()
    for i, line in enumerate(code_lines):
        if line.startswith("from temp_project"):
            code_lines[i] = line.replace('temp_project', project_name)
    code_path.write_text('\n'.join(code_lines) + '\n')


def create_default_project(
    name: str,
    project_dir: Path,
) -> None:
    def modify_cfg_test():
        _replace_import(project_dir.joinpath("tests/test_cfg.py"), name)

    def modify_log_test():
        _replace_import(project_dir.joinpath("tests/test_log.py"), name)

    def modify_main_test():
        _replace_import(project_dir.joinpath("tests/test_main.py"), name)

    template_dir = STUBS_ROOT.joinpath("template-project-default")
    shutil.copytree(template_dir, project_dir)
    shutil.move(project_dir / "src" / "name", project_dir / "src" / name)
    modify_toml(project_dir.joinpath("pyproject.toml"), name)
    modify_cfg(project_dir.joinpath(f"src/{name}/_cfg.py"), name)
    modify_cfg_test()
    modify_log_test()
    modify_main_test()


def create_fastapi_project(
    name: str,
    project_dir: Path,
) -> None:

    def modify_app():
        _replace_import(project_dir.joinpath(f"src/{name}/app.py"), name)

    def modify_cfg_test():
        _replace_import(project_dir.joinpath("tests/test_cfg.py"), name)

    def modify_log_test():
        _replace_import(project_dir.joinpath("tests/test_log.py"), name)

    def modify_server_test():
        _replace_import(project_dir.joinpath("tests/test_server.py"), name)

    template_dir = STUBS_ROOT.joinpath("template-project-fastapi")
    shutil.copytree(template_dir, project_dir)
    shutil.move(project_dir / "src" / "name", project_dir / "src" / name)
    modify_toml(project_dir.joinpath("pyproject.toml"), name)
    modify_cfg(project_dir.joinpath(f"src/{name}/_cfg.py"), name)
    modify_app()
    modify_cfg_test()
    modify_log_test()
    modify_server_test()


def update_vscode_settings(dst_path: Path):
    template_dir = STUBS_ROOT.joinpath("template-project-default")
    src_path = template_dir.joinpath(".vscode/settings.json")

    # backup th old
    shutil.copyfile(
        dst_path,
        dst_path.parent.joinpath(f"{dst_path.stem}_back{format_now()}{dst_path.suffix}"),
    )
    shutil.copyfile(src_path, dst_path)


app = typer.Typer()


@app.command("c", help="Alias for create")
@app.command("create")
def create(
    project_path: Annotated[
        str,
        typer.Option("--path", "-p", help="Path to project root."),
    ],
    project_type: Annotated[
        Optional[str],
        typer.Option("--type", "-t", help="Type of project"),
    ] = None,
):
    """Create project."""

    name, project_dir = normalize_path(
        project_path, name_process_fn=lambda x: inflection.underscore(x.strip())
    )

    if project_dir.exists():
        Notifier.exists(str(project_dir))
        Notifier.exited()
        return

    if project_type is None:
        create_default_project(name, project_dir)
        Notifier.create_success(str(project_dir))
        Notifier.exited()
    elif project_type == 'fastapi':
        create_fastapi_project(name, project_dir)
        Notifier.create_success(str(project_dir))
        Notifier.exited()
    else:
        # TODO
        Notifier.exited()


@app.command("ss", help="Alias for sync-settings")
@app.command("sync-settings")
def sync_settings(
    project_path: Annotated[
        Optional[str],
        typer.Option("--path", "-p", help="Path to project root."),
    ] = None
):
    """Sync vscode settings to the latest template."""
    if project_path is None:
        setting_path = ".vscode/settings.json"
    else:
        name, project_dir = normalize_path(project_path)
        # TODO:
        pass
    dst_path = get_absolute_cwd_path().joinpath(setting_path)
    if not dst_path.exists():
        Notifier.not_exists(str(dst_path))
        Notifier.exited()
    else:
        update_vscode_settings(dst_path)
        Notifier.update_success(str(dst_path))
        Notifier.exited()
