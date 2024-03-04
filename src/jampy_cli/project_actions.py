import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from rich import print as rprint

from .common_utils import get_absolute_cwd, get_datetime, parse_name_to_absolute_path
from .config import Config
from .notifier import Notifier


def create_default_project(
    name: str,
    project_dir: Path,
) -> None:
    template_dir = Config.STUBS_ROOT.joinpath('template-project-default')
    toml_str = template_dir.joinpath('pyproject.toml').read_text()
    toml_cfg = toml.loads(toml_str)
    toml_cfg['project']['name'] = name
    toml_cfg['project']['scripts'] = {'run': f'{name}.main:main'}
    toml_cfg['tool']['setuptools']['packages']['find']['include'] = [f'{name}*']
    template_dir.joinpath('pyproject.toml').write_text(toml.dumps(toml_cfg))
    shutil.copytree(template_dir, project_dir)
    shutil.move(project_dir / 'src' / 'name', project_dir / 'src' / name)


def update_vscode_settings(dst_path: Path):
    template_dir = Config.STUBS_ROOT.joinpath('template-project-default')
    src_path = template_dir.joinpath('.vscode/settings.json')

    # backup th old
    shutil.copyfile(
        dst_path,
        dst_path.parent.joinpath(f"{dst_path.stem}_back{get_datetime()}{dst_path.suffix}"),
    )
    shutil.copyfile(src_path, dst_path)


app = typer.Typer()


@app.command('c', help='Alias for create')
@app.command('create')
def create(
    project_path: Annotated[
        str,
        typer.Option('--path', '-p', help='Path to project root.'),
    ],
    project_type: Annotated[
        Optional[str],
        typer.Option("--type", "-t", help='Type of project'),
    ] = None,
):
    """Create project."""

    name, project_dir = parse_name_to_absolute_path(
        project_path, name_process_fn=lambda x: inflection.underscore(x.strip())
    )

    if project_dir.exists():
        Notifier.exists(rprint, str(project_dir))
        Notifier.exited(rprint)
        return

    if project_type is None:
        create_default_project(name, project_dir)
        Notifier.create_success(rprint, str(project_dir))
        Notifier.exited(rprint)
    else:
        # TODO
        Notifier.exited(rprint)


@app.command('ss', help='Alias for sync-settings')
@app.command('sync-settings')
def sync_settings(
    project_path: Annotated[
        Optional[str], typer.Option('--path', '-p', help='Path to project root.')
    ] = None
):
    """Sync vscode settings to the latest template."""
    if project_path is None:
        setting_path = '.vscode/settings.json'
    else:
        name, project_dir = parse_name_to_absolute_path(project_path)
        # TODO:
        pass
    dst_path = get_absolute_cwd().joinpath(setting_path)
    if not dst_path.exists():
        Notifier.not_exists(rprint, str(dst_path))
        Notifier.exited(rprint)
    else:
        update_vscode_settings(dst_path)
        Notifier.update_success(rprint, str(dst_path))
        Notifier.exited(rprint)
