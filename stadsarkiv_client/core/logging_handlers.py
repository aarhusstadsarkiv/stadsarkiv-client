"""
A couple of logging handlers.
"""

from typing import Any
import logging
import os
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler
import warnings
from stadsarkiv_client.core.args import get_data_dir
import json

MAX_LOG_SIZE = 100 * 1024 * 1024
BACKUP_COUNT = 5
warnings.simplefilter(action="ignore", category=FutureWarning)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # If exception information is present, add it to the log record
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Add extra fields to the log record if they exist
        extra_fields = {
            "error_code": "error_code",
            "error_type": "error_type",
            "error_url": "error_url",
            "exception": "exception",
            "message": "message",
        }

        for attr, log_key in extra_fields.items():
            value = getattr(record, attr, None)
            if value:
                log_record[log_key] = value

        return json.dumps(log_record)


def generate_log_dir():
    log_dir = get_data_dir("logs")
    os.makedirs(log_dir, exist_ok=True)


def get_rotating_json_file_handler(level: Any, file_name):
    Path(file_name).touch()
    handler = ConcurrentRotatingFileHandler(file_name, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    handler.setLevel(level)
    handler.setFormatter(JsonFormatter())
    return handler


def get_stream_handler(level: Any):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(JsonFormatter())
    return ch


def get_rotating_file_handler(level: Any, file_name):
    Path(file_name).touch()
    handler = ConcurrentRotatingFileHandler(file_name, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
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
