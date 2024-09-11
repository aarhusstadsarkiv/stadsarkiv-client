"""
This file exposes get_local_config_dir() to the rest of the application.
config-dir can be set on the command line with --config-dir
It is then added to the environment. This function will return the value of CONFIG_DIR
or "local" if it is not set.
"""

import os
from stadsarkiv_client.core.logging_handlers import get_init_logger


log = get_init_logger()


def get_local_config_dir(*sub_dirs: str) -> str:
    """
    Get a config dir from command line arguments.
    If it is not set, return "local".
    """
    # Get env CONFIG_DIR from os. This is set in the command line arguments to the server.

    local_config_dir = os.environ.get("CONFIG_DIR", "local")

    # join the sub_dirs to the local_config_dir
    paths = os.path.join(local_config_dir, *sub_dirs)

    return paths
