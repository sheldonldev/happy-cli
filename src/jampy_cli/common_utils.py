import importlib.metadata
import os
import posixpath
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple


def parse_path_str(
    raw_path: str,
    name_process_fn: Optional[Callable] = None,
) -> Tuple[str, Path]:
    parsed_path = Path(raw_path).expanduser()
    name, parent, root = parsed_path.name, str(parsed_path.parent), parsed_path.root
    if name_process_fn is not None:
        name = name_process_fn(name)
    if root == '/':
        absolute_path = Path(parent).joinpath(name)
    elif parent == '.':
        absolute_path = get_absolute_cwd().joinpath(name)
    else:
        absolute_path = Path(posixpath.normpath(get_absolute_cwd().joinpath(parent).joinpath(name)))
    return name, absolute_path


def get_absolute_cwd() -> Path:
    return Path(os.path.abspath(os.getcwd()))


def get_datetime(format: str = '%Y%m%d_%H%M%S', utc: bool = True) -> str:
    if utc is True:
        return f'{datetime.utcnow().strftime(format)}_UTC'
    else:
        return f'{datetime.now().strftime(format)}'


def get_package_info(package_name: str) -> Dict:
    try:
        metadata = importlib.metadata.metadata(package_name)
        return metadata.json
    except importlib.metadata.PackageNotFoundError as e:
        raise e
