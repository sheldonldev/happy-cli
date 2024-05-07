from pathlib import Path

from util_common.package import get_package_info

APP_NAME = 'util_common'
__info__ = get_package_info(APP_NAME)

VERSION = __info__.get('version')

AUTHOR_NAME = None
AUTHOR_EMAIL = None
authors = __info__.get('authors')
if isinstance(authors, list) and len(authors) > 0:
    AUTHOR_NAME = authors[0].get('name')
    AUTHOR_EMAIL = authors[0].get('email')

STUBS_ROOT = Path(__file__).parent.joinpath('stubs')
