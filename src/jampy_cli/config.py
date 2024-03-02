from pathlib import Path


class Config:
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    STUBS_ROOT = Path(__file__).parent.joinpath('stubs')
