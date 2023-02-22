import logging
import os

log_level = logging.DEBUG

if os.getenv("ENVIRONMENT") == "production":
    log_level = logging.INFO

settings = {
    "log_level": log_level
}