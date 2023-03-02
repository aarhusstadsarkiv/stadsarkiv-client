import logging
import os
from pathlib import Path
from .dynamic_settings import settings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def generate_log_dir():
    dir = "./logs"
    os.makedirs(dir, exist_ok=True)
    Path('./logs/main.log').touch()


if 'file' in settings["log_handlers"]:
    generate_log_dir()


log = logging.getLogger("main")
level = settings["log_level"]
log.setLevel(level)


def get_file_handler():
    fh = logging.FileHandler('logs/main.log')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh


def get_stream_handler():
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch


if not len(log.handlers):

    if 'file' in settings["log_handlers"]:
        fh = get_file_handler()
        log.addHandler(fh)

    if 'stream' in settings["log_handlers"]:
        ch = get_stream_handler()
        log.addHandler(ch)
