"""
A couple of logging handlers.
"""

from typing import Any
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def generate_log_dir():
    dir = "./logs"
    os.makedirs(dir, exist_ok=True)
    Path("./logs/main.log").touch()


def get_file_handler(level: Any):
    fh = logging.FileHandler("logs/main.log")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh


def get_stream_handler(level: Any):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch


def get_rotating_file_handler(level: Any):
    handler = RotatingFileHandler("logs/main.log", maxBytes=10 * 1024 * 1024, backupCount=10)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def get_init_logger():
    """Init logger to use before settings are loaded"""

    log = logging.getLogger("env")
    if not len(log.handlers):
        level = logging.DEBUG
        log.setLevel(level)
        ch = get_stream_handler(level)
        log.addHandler(ch)

    return log
