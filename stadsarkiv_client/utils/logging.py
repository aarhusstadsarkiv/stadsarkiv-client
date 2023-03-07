import logging
from .dynamic_settings import settings
from .logging_defs import get_file_handler, get_stream_handler, generate_log_dir
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


log = logging.getLogger("main")
level = settings["log_level"]
log.setLevel(level)


if not len(log.handlers):

    if 'file' in settings["log_handlers"]:
        generate_log_dir()
        fh = get_file_handler(level)
        log.addHandler(fh)

    if 'stream' in settings["log_handlers"]:
        ch = get_stream_handler(level)
        log.addHandler(ch)


def get_log() -> logging.Logger:
    return log


__ALL__ = [get_log]
