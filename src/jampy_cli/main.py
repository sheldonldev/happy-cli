from typing import Optional

import toml
import typer
from rich import print as rprint
from typing_extensions import Annotated

from . import module_actions, project_actions
from .config import Config

__info__ = toml.loads(Config.PROJECT_ROOT.joinpath('pyproject.toml').read_text())


def version_callback(value: bool):
    if value:
        rprint(f"Awesome Jampy CLI Version: {__info__['project']['version']}")
        raise typer.Exit()


app = typer.Typer(
    add_completion=True,
    pretty_exceptions_show_locals=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback()
def call_version(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback),
    ] = None,
):
    pass


@app.command('i', help='Alias for "info".')
@app.command('info')
def show_info():
    """Show the project toml."""
    rprint(toml.dumps(__info__))


def gen_help(message):
    return f'{message} Use -h to see more.'


app.add_typer(
    project_actions.app,
    name='project',
    help=gen_help('Project actions.'),
)
app.add_typer(
    module_actions.app,
    name='module',
    help=gen_help('Module actions.'),
)
