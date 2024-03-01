import os
import shutil
from pathlib import Path

from typer.testing import CliRunner

from happy_cli import app


def test_create_project():
    runner = CliRunner()
    name = "temp_project"
    project_dir = Path(f"{os.path.abspath(os.getcwd())}/{name}")
    if project_dir.exists():
        shutil.rmtree(project_dir)

    result = runner.invoke(app, ["create-project", name])
    assert result.exit_code == 0
    assert Path(f"{os.path.abspath(os.getcwd())}/{name}").exists() is True


if __name__ == '__main__':
    test_create_project()
