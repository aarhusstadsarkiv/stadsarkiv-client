"""
A couple of logging handlers.
"""

from typing import Any
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import warnings
from stadsarkiv_client.core.args import get_data_dir

warnings.simplefilter(action="ignore", category=FutureWarning)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def generate_log_dir():
    log_dir = get_data_dir("logs")
    os.makedirs(log_dir, exist_ok=True)


def get_stream_handler(level: Any):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch


def get_rotating_file_handler(level: Any, file_name):
    Path(file_name).touch()
    handler = RotatingFileHandler(file_name, maxBytes=10 * 1024 * 1024, backupCount=10)
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
