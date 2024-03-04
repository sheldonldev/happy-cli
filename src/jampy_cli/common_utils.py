import importlib.metadata
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple


def parse_name_to_absolute_path(
    raw_name: str,
    name_process_fn: Optional[Callable] = None,
    **kwargs,
) -> Tuple[str, Path]:
    parsed_name = Path(raw_name)
    name, parent, root = parsed_name.name, str(parsed_name.parent), parsed_name.root
    if name_process_fn is not None:
        name = name_process_fn(name, **kwargs)
    if root == '/':
        absolute_path = Path(parent).joinpath(name)
    elif parent == '.':
        absolute_path = get_absolute_cwd().joinpath(name)
    else:
        absolute_path = get_absolute_cwd().joinpath(parent).joinpath(name)
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
