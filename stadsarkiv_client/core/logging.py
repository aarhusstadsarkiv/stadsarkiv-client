from typing import Any
import logging
from .dynamic_settings import settings
from .logging_defs import get_file_handler, get_stream_handler, generate_log_dir
import warnings
import inspect

warnings.simplefilter(action="ignore", category=FutureWarning)


log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)


class customHandler(logging.Handler):
    def emit(self, record):
        pass


if not len(log.handlers):
    # log.addHandler(customHandler())
    if "file" in settings["log_handlers"]:  # type: ignore
        generate_log_dir()
        fh = get_file_handler(level)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:  # type: ignore
        ch = get_stream_handler(level)
        log.addHandler(ch)


def get_log() -> logging.Logger:
    return log
