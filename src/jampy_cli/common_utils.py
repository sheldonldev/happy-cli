import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Tuple


def parse_name_to_path(
    raw_name: str,
    postprocess_fn: Optional[Callable] = None,
    **kwargs,
) -> Tuple[str, Path]:
    parsed_name = Path(raw_name)
    name, parent, root = parsed_name.name, str(parsed_name.parent), parsed_name.root
    if postprocess_fn is not None:
        name = postprocess_fn(name, **kwargs)
    if root == '/':
        project_dir = Path(parent).joinpath(name)
    elif parent == '.':
        project_dir = get_cwd().joinpath(name)
    else:
        project_dir = get_cwd().joinpath(parent).joinpath(name)
    return name, project_dir


def get_cwd() -> Path:
    return Path(os.path.abspath(os.getcwd()))


def get_datetime(format: str = '%Y%m%d_%H%M%S', utc: bool = True) -> str:
    if utc is True:
        return f'{datetime.utcnow().strftime(format)}_UTC'
    else:
        return f'{datetime.now().strftime(format)}'
