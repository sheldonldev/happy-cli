import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from rich import print as rprint

from .common_utils import parse_path_str
from .config import Config
from .notifier import Notifier


def create_default_module(
    name: str,
    module_dir: Path,
) -> None:
    def modify_toml():
        toml_str = template_dir.joinpath('pyproject.toml').read_text()
        toml_cfg = toml.loads(toml_str)
        toml_cfg['project']['name'] = name
        template_dir.joinpath('pyproject.toml').write_text(toml.dumps(toml_cfg))

    def modify_init():
        template_dir.joinpath('src/__init__.py').write_text(
            f'from .main import main as {name}\n'
        )
        template_dir.joinpath('__init__.py').write_text(
            f'from .src import {name}\n'
        )

    template_dir = Config.STUBS_ROOT.joinpath('template-module-default')
    modify_toml()
    modify_init()
    shutil.copytree(template_dir, module_dir)


app = typer.Typer()


@app.command('c', help='Alias for create')
@app.command('create')
def create(
    module_path: Annotated[
        str,
        typer.Option('--path', '-p', help='Path to module root.'),
    ],
    module_type: Annotated[
        Optional[str], typer.Option("--type", "-t", help='Type of module.')
    ] = None,
) -> None:
    """Create module."""

    name, module_dir = parse_path_str(
        module_path, name_process_fn=lambda x: inflection.underscore(x.strip())
    )

    if module_dir.exists():
        Notifier.exists(rprint, str(module_dir))
        Notifier.exited(rprint)
        return

    if module_type is None:
        create_default_module(name, module_dir)
        Notifier.create_success(rprint, str(module_dir))
        Notifier.exited(rprint)
    else:
        # TODO
        Notifier.exited(rprint)
