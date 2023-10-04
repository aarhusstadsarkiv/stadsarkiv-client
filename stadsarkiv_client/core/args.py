"""
This file reads command line arguments that may be used in the application.
"""

import os
from stadsarkiv_client.core.logging_handlers import get_init_logger


log = get_init_logger()


def get_local_config_dir(*sub_dirs: str) -> str:
    """
    Get a config dir from command line arguments.
    If it is not set, return "local".
    If set check if it exists. If not just log a warning.
    """
    # Get env CONFIG_DIR from os
    local_config_dir = os.environ.get("CONFIG_DIR", "local")

    # Use *sub_dirs to unpack the list of subdirectories
    return os.path.join(local_config_dir, *sub_dirs)
