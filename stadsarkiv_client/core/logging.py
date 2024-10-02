"""
Set up a single logger for the application.
Contains a single function (get_log) that returns the setup logger.
"""

from typing import Any
import logging
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import logging_handlers
import warnings


logging_handlers.generate_log_dir()

warnings.simplefilter(action="ignore", category=FutureWarning)

# remove uvicorn noise in debug mode
if settings["environment"] == "development":
    logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)

log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)

if not len(log.handlers):

    if "file" in settings["log_handlers"]:
        log.debug("Logging to file enabled")
        fh = logging_handlers.get_file_handler(level, file_name="logs/main.log")
        log.addHandler(fh)

    if "rotating_file" in settings["log_handlers"]:
        log.debug("Logging to rotating file enabled")
        fh = logging_handlers.get_rotating_file_handler(level, file_name="logs/main.log")
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:
        log.debug("Logging to stream enabled")
        ch = logging_handlers.get_stream_handler(level)
        log.addHandler(ch)

access_log = logging.getLogger("access")
level = settings["log_level"]
access_log.setLevel(level)

if not len(access_log.handlers):
    fh = logging_handlers.get_rotating_file_handler(level, file_name="logs/access.log")
    access_log.addHandler(fh)


def get_log() -> logging.Logger:
    return log


def get_access_log() -> logging.Logger:
    return access_log
