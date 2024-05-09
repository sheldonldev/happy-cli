import shutil
from pathlib import Path
from typing import Annotated

import inflection
import typer
from util_common.path import normalize_path

from ._cfg import STUBS_ROOT
from .notifier import Notifier


def create_swift_project(project_dir: Path):
    template_dir = STUBS_ROOT.joinpath("template-workspace-swift")
    shutil.copytree(template_dir, project_dir)


app = typer.Typer()


@app.command("c", help="Alias for create")
@app.command("create")
def create(
    workspace_path: Annotated[
        str,
        typer.Option("--path", "-p", help="Path to workspace root."),
    ],
    workspace_type: Annotated[
        str,
        typer.Option("--type", "-t", help="Type of workspace."),
    ],
):
    name, workspace_dir = normalize_path(
        workspace_path,
        name_process_fn=lambda x: inflection.underscore(x.strip()),
    )

    if workspace_dir.exists():
        Notifier.exists(str(workspace_dir))
        Notifier.exited()
        return

    if workspace_type == 'swift':
        create_swift_project(workspace_dir)
        Notifier.create_success(str(workspace_dir))
        Notifier.exited()
