import subprocess
from typing import Annotated, Optional

import typer

from ._cfg import AUTHOR_EMAIL, AUTHOR_NAME
from .notifier import Notifier

app = typer.Typer()


@app.command("ia", help="Alias for init-account")
@app.command("init-account")
def init_account(
    user_name: Annotated[
        Optional[str],
        typer.Option("--user-name", "-un", help="GitHub user name."),
    ] = None,
    user_email: Annotated[
        Optional[str],
        typer.Option("--user-email", "-ue", help="GitHub user email."),
    ] = None,
):
    if user_name is None:
        if AUTHOR_NAME is None:
            Notifier.not_exists('--user-name')
            Notifier.exited()
            return
        user_name = AUTHOR_NAME
    if user_email is None:
        if AUTHOR_EMAIL is None:
            Notifier.not_exists('--user-email')
            Notifier.exited()
            return
        user_email = AUTHOR_EMAIL

    subprocess.run(
        f'git config --global user.name {user_name}',
        shell=True,
    )
    subprocess.run(
        f'git config --global user.email {user_email}',
        shell=True,
    )
    subprocess.run(
        f'ssh-keygen -t rsa -C {user_email}',
        shell=True,
    )
    subprocess.run(
        'cat ~/.ssh/id_rsa.pub',
        shell=True,
    )
