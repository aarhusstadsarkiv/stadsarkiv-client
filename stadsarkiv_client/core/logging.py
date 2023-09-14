from typing import Any
import logging
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import logging_defs
import warnings


warnings.simplefilter(action="ignore", category=FutureWarning)


log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)


if not len(log.handlers):
    if "file" in settings["log_handlers"]:  # type: ignore
        log.debug("Logging to file enabled")
        logging_defs.generate_log_dir()
        fh = logging_defs.get_file_handler(level)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:  # type: ignore
        log.debug("Logging to stream enabled")
        ch = logging_defs.get_stream_handler(level)
        log.addHandler(ch)


def get_log() -> logging.Logger:
    return log
