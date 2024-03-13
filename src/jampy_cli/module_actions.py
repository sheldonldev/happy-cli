import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from jampy_util.path import normalize_path
from rich import print as print

from .config import Config
from .notifier import Notifier


def create_default_module(
    name: str,
    module_dir: Path,
) -> None:
    def modify_toml():
        toml_str = module_dir.joinpath('pyproject.toml').read_text()
        toml_cfg = toml.loads(toml_str)
        toml_cfg['project']['name'] = name
        module_dir.joinpath('pyproject.toml').write_text(toml.dumps(toml_cfg))

    def modify_init():
        module_dir.joinpath('src/__init__.py').write_text(
            f'from .main import main as {name}\n\n__all__ = ["{name}"]\n'
        )
        module_dir.joinpath('__init__.py').write_text(
            f'from .src import {name}\n\n__all__ = ["{name}"]\n'
        )

    template_dir = Config.STUBS_ROOT.joinpath('template-module-default')
    shutil.copytree(template_dir, module_dir)
    modify_toml()
    modify_init()


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

    name, module_dir = normalize_path(
        module_path, name_process_fn=lambda x: inflection.underscore(x.strip())
    )

    if module_dir.exists():
        Notifier.exists(print, str(module_dir))
        Notifier.exited(print)
        return

    if module_type is None:
        create_default_module(name, module_dir)
        Notifier.create_success(print, str(module_dir))
        Notifier.exited(print)
    else:
        # TODO
        Notifier.exited(print)
