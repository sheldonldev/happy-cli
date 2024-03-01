import os
import subprocess
from importlib.metadata import version
from pathlib import Path
from typing import Optional

import inflection
import toml
import typer
from rich import print as rprint

__version__ = "0.1.2"


def version_callback(value: bool):
    if value:
        typer.echo(f"Awesome Happy CLI Version: {__version__}")
        raise typer.Exit()


app = typer.Typer(add_completion=False)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
    ),
):
    pass


@app.command('info')
def show_info():
    rprint("My happy cli.")


@app.command("create-project")
def create_project(
    name: Optional[str] = typer.Argument(None),
):
    if name is None:
        rprint("project name not given!")
        rprint("Exited!")
        return
    target = os.path.abspath(os.getcwd())
    project_dir = Path(f'{target}/{name}')
    if project_dir.exists():
        rprint(f"{project_dir} already exists!")
        rprint("Exited!")
        return
    else:
        stubs_dir = Path(__file__).parent.joinpath('stubs')
        template_dir = stubs_dir.joinpath('template-empty')
        toml_str = template_dir.joinpath('pyproject.toml').read_text()
        toml_cfg = toml.loads(toml_str)
        toml_cfg['project']['name'] = name

        name = inflection.underscore(name.strip())
        toml_cfg['project']['scripts'] = {'run': f'{name}.main:main'}
        toml_cfg['tool']['setuptools']['packages']['find']['include'] = [f'{name}*']
        template_dir.joinpath('pyproject.toml').write_text(toml.dumps(toml_cfg))
        subprocess.run(f"cp -r {template_dir} {project_dir}", shell=True)
        subprocess.run(f"mv {project_dir}/src/project_name {project_dir}/src/{name}", shell=True)
        rprint(f"{project_dir} created successfully!")
