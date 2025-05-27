"""
This module sets up and configures application-wide logging for the Maya core system.

It defines and initializes two main loggers: a general-purpose logger (`main`) and an access logger (`access`).
Logging behavior is controlled by dynamic runtime settings from `maya.core.dynamic_settings.settings`,
which specify the log level and the enabled log handlers (e.g., stream and rotating file handlers).

Key functionalities:
- Suppresses `FutureWarning` messages to keep logs clean.
- Disables lower-level logging from the `uvicorn.error` logger by setting its level to CRITICAL.
- Ensures that log directories are created before logging begins via `generate_log_dir()`.
- Sets up log handlers conditionally based on settings, including rotating JSON file handlers and stream handlers.
- Provides access to the configured loggers via `get_log()` and `get_access_log()` functions.

Functions:
- `get_log()`: Returns the main application logger.
- `get_access_log()`: Returns the access logger.

"""

from typing import Any
import logging
from maya.core.dynamic_settings import settings
from maya.core import logging_handlers
import warnings
from maya.core.paths import get_data_dir_path


logging_handlers.generate_log_dir()
warnings.simplefilter(action="ignore", category=FutureWarning)
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)

log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)

if not len(log.handlers):

    if "rotating_file" in settings["log_handlers"]:
        log.debug("Logging to rotating file enabled")
        main_file_name = get_data_dir_path("logs", "main.log")
        fh = logging_handlers.get_rotating_json_file_handler(level, file_name=main_file_name)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:
        log.debug("Logging to stream enabled")
        ch = logging_handlers.get_stream_handler(level)
        log.addHandler(ch)

access_log = logging.getLogger("access")
level = settings["log_level"]
access_log.setLevel(level)

if not len(access_log.handlers):
    access_file_name = get_data_dir_path("logs", "access.log")
    fh = logging_handlers.get_rotating_file_handler(level, file_name=access_file_name)
    access_log.addHandler(fh)


def get_log() -> logging.Logger:
    return log


def get_access_log() -> logging.Logger:
    return access_log
