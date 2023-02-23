import logging
import os


log_level = logging.INFO

if os.getenv("ENVIRONMENT") == "development":
    log_level = logging.DEBUG

settings = {
    "log_level": log_level
}