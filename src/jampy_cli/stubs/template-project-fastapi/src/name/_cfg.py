import importlib.metadata
import os
from pathlib import Path

APP_NAME = "temp_project"
__info__ = importlib.metadata.metadata(APP_NAME)
VERSION = __info__.get("version")
AUTHOR_EMAIL = __info__.get("author_email")

DATA_ROOT = Path(
    os.environ.get("DATA_ROOT", str(Path(__file__).parent.parent.parent.joinpath('data')))
)
LOG_DIR = DATA_ROOT.joinpath('log')

IS_DEBUG = os.environ.get("IS_DEBUG", "False")
