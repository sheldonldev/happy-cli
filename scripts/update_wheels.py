import os
import posixpath
import shutil
from pathlib import Path
from typing import Callable, Optional, Tuple

import toml
from config import Config
from jampy_utils.path import parse_path_str


def parse_wheel_path(
    repo_dir: Path,
) -> Tuple[Optional[str], Optional[str], Optional[Path]]:
    package_name, file_name, file_path = None, None, None
    toml_cfg = toml.loads(repo_dir.joinpath('pyproject.toml').read_text())
    package_name = toml_cfg['project']['name']
    version = toml_cfg['project']['version']
    wheels = [
        x for x in repo_dir.joinpath('dist').glob('*.whl') if version in str(x)
    ]
    if len(wheels) == 1:
        file_path = wheels[0]
        file_name = file_path.name
    return package_name, file_name, file_path


def update_wheels(package_name, src_file_path: Path) -> None:
    dst_dir = Config.PROJECT_ROOT.joinpath('wheels')
    for wheel_path in dst_dir.glob(f"{package_name}-*.whl"):
        os.remove(wheel_path)
    shutil.copy2(src_file_path, dst_dir)


def update_install_wheels_bash(package_name: str) -> None:
    bash_path = Config.PROJECT_ROOT.joinpath('install_wheels.sh')
    commands = [
        x.strip()
        for x in bash_path.read_text().splitlines()
        if (x.startswith('pip') and package_name not in x)
    ]
    commands.append(f'pip install --find-links="./wheels" {package_name}')
    bash_path.write_text("#!/bin/bash\n" + "\n".join(commands))


def main(repo_path_str: str) -> None:
    _, repo_dir = parse_path_str(repo_path_str)
    package_name, _, wheel_path = parse_wheel_path(repo_dir)
    if wheel_path is None or package_name is None:
        raise FileNotFoundError(f'wheels of {repo_path_str} not found!')
    update_wheels(package_name, wheel_path)
    update_install_wheels_bash(package_name)


if __name__ == '__main__':
    for repo in [
        "~/repos/jampy_utils",
    ]:
        main(repo)
