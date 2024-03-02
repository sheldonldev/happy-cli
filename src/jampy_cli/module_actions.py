import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from rich import print as rprint

from .common_utils import parse_name_to_absolute_path
from .config import Config
from .notifier import Notifier


def create_default_module(
    name: str,
    module_dir: Path,
) -> None:
    template_dir = Config.STUBS_ROOT.joinpath('template-module-default')
    toml_str = template_dir.joinpath('pyproject.toml').read_text()
    toml_cfg = toml.loads(toml_str)
    toml_cfg['project']['name'] = name
    template_dir.joinpath('pyproject.toml').write_text(toml.dumps(toml_cfg))

    shutil.copytree(template_dir, module_dir)
    shutil.move(module_dir / 'src' / 'name', module_dir / 'src' / name)


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

    name, module_dir = parse_name_to_absolute_path(
        module_path, postprocess_fn=lambda x: inflection.underscore(x.strip())
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
