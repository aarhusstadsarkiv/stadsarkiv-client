from typing import Any
import logging
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import logging_defs
import warnings

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
        logging_defs.generate_log_dir()
        fh = logging_defs.get_file_handler(level)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:  # type: ignore
        ch = logging_defs.get_stream_handler(level)
        log.addHandler(ch)


def get_log() -> logging.Logger:
    return log
