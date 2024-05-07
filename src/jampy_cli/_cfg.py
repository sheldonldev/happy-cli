from pathlib import Path

from util_common.package import get_package_info

APP_NAME = 'util_common'
__info__ = get_package_info(APP_NAME)

VERSION = __info__.get('version')

AUTHOR_NAME = None
AUTHOR_EMAIL = None
author_email = __info__.get('author_email')
if isinstance(author_email, str) and len(author_email) > 0:
    if len(author_email.split()) > 1:
        author, email = author_email.split()[:2]
        AUTHOR_NAME = author
        AUTHOR_EMAIL = email.lstrip('<').rstrip('>')

STUBS_ROOT = Path(__file__).parent.joinpath('stubs')
