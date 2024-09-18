import logging
from typing import cast

from temp_project._cfg import APP_NAME, IS_DEBUG, LOG_DIR
from util_common.io import parse_bool
from util_common.logger import LogSettings, _LogLevel, setup_loggers


def init_log():
    log_dir = LOG_DIR.joinpath(APP_NAME)
    logger_names = [
        None,
        APP_NAME,
    ]
    if parse_bool(IS_DEBUG) is True:
        level = 'debug'
    else:
        level = 'info'
    log_settings_list = [
        LogSettings(
            name=name,
            save_file_or_dir=log_dir,
            rich_handler=True,
            json_logger=True,
            level=cast(_LogLevel, level),
        )
        for name in logger_names
    ]
    setup_loggers(log_settings_list)


init_log()
log = logging.getLogger(APP_NAME)
