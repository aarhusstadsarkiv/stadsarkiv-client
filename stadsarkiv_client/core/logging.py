"""
Set up a single logger for the application.
Contains a single function (get_log) that returns the setup logger.
"""

from typing import Any
import logging
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import logging_handlers
import warnings
from stadsarkiv_client.core.args import get_data_dir


logging_handlers.generate_log_dir()
warnings.simplefilter(action="ignore", category=FutureWarning)

# remove uvicorn noise in debug mode
# if settings["environment"] == "development":
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)

log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)

if not len(log.handlers):

    if "rotating_file" in settings["log_handlers"]:
        log.debug("Logging to rotating file enabled")
        main_file_name = get_data_dir("logs", "main.log")
        fh = logging_handlers.get_rotating_file_handler(level, file_name=main_file_name)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:
        log.debug("Logging to stream enabled")
        ch = logging_handlers.get_stream_handler(level)
        log.addHandler(ch)

access_log = logging.getLogger("access")
level = settings["log_level"]
access_log.setLevel(level)

if not len(access_log.handlers):
    access_file_name = get_data_dir("logs", "access.log")
    fh = logging_handlers.get_rotating_file_handler(level, file_name=access_file_name)
    access_log.addHandler(fh)


def get_log() -> logging.Logger:
    return log


def get_access_log() -> logging.Logger:
    return access_log
