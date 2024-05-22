import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from util_common.path import normalize_path

from ._cfg import STUBS_ROOT
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
        module_dir.joinpath('__init__.py').write_text(
            f'from .src.main import main as {name}\n\n__all__ = ["{name}"]\n'
        )

    def modify_test():
        shutil.move(
            module_dir.joinpath('tests/test_main.py'),
            module_dir.joinpath(f'tests/test_{name}.py'),
        )

    template_dir = STUBS_ROOT.joinpath('template-module-default')
    shutil.copytree(template_dir, module_dir)
    modify_toml()
    modify_init()
    modify_test()


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
        Notifier.exists(str(module_dir))
        Notifier.exited()
        return

    if module_type is None:
        create_default_module(name, module_dir)
        Notifier.create_success(str(module_dir))
        Notifier.exited()
    else:
        # TODO
        Notifier.exited()
