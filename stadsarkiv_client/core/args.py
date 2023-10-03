"""
This file reads command line arguments that may be used in the application.
"""

import os
from stadsarkiv_client.core.logging_handlers import get_init_logger


log = get_init_logger()


def get_config_dir():
    """
    Get a config dir from command line arguments.
    If it is not set, return "local".
    If set check if it exists. If not just log a warning.
    """
    # Get env CONFIG_DIR from os
    return os.environ.get("CONFIG_DIR", "local")
