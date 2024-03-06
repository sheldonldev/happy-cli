import os
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Callable, Optional, Tuple

import toml
from config import Config
from jampy_util.path import normalize_path


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
    if (dst_dir.exists() is True) and (dst_dir.is_dir() is True):
        for wheel_path in dst_dir.glob(f"{package_name}-*.whl"):
            os.remove(wheel_path)
        shutil.copyfile(src_file_path, dst_dir.joinpath(src_file_path.name))
        return
    with suppress(FileNotFoundError):
        os.remove(dst_dir)
    dst_dir.mkdir()
    shutil.copyfile(src_file_path, dst_dir.joinpath(src_file_path.name))


def update_install_wheels_bash(package_name: str) -> None:
    bash_path = Config.PROJECT_ROOT.joinpath('install_wheels.sh')
    bash_lines = [
        "#!/bin/bash",
        "python scripts/update_wheels.py",
    ]
    commands = [
        x.strip()
        for x in bash_path.read_text().splitlines()
        if (x.startswith('pip') and package_name not in x)
    ]
    commands.append(f'pip install --find-links="./wheels" {package_name}')
    bash_lines.extend(commands)
    bash_path.write_text("\n".join(bash_lines))


def main(package_path_str: str) -> None:
    _, repo_dir = normalize_path(package_path_str)
    package_name, _, wheel_path = parse_wheel_path(repo_dir)
    if wheel_path is None or package_name is None:
        raise FileNotFoundError(f'wheels of {package_path_str} not found!')
    update_wheels(package_name, wheel_path)
    update_install_wheels_bash(package_name)


if __name__ == '__main__':
    for package in [
        "~/repos/sheldon/jampy_util/jampy_util",
        "~/repos/sheldon/jampy_util/jampy_util_intelligence",
    ]:
        main(package)
