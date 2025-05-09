"""
This file exposes get_local_config_dir() and get_data_dir to the rest of the application.

The config-dir can be set on the command line with --config-dir
It is then added to the environment. This function will return the value of CONFIG_DIR
or "local" if it is not set.

The data-dir can be set on the command line with --data-dir and is added to the environment.
This function will return the value of DATA_DIR or "data" if it is not set.
"""

import os


def get_local_config_dir(*sub_dirs: str) -> str:
    """
    Get a config dir from command line arguments.
    If it is not set, return "local".
    """
    # Get env CONFIG_DIR from os. This is set in the command line arguments to the server.
    config_dir = os.environ.get("CONFIG_DIR")

    # raise an error if the config dir is not set
    if config_dir is None:
        raise ValueError("CONFIG_DIR is not set. Please set it to a valid directory.")

    # join the sub_dirs to the local_config_dir
    paths = os.path.join(config_dir, *sub_dirs)

    return paths


def get_data_dir(*sub_dirs: str) -> str:
    """
    Get a data dir from command line arguments.
    If it is not set, return "data".
    """
    config_dir = get_local_config_dir()
    local_data_dir = os.path.join(config_dir, "data")

    return os.path.join(local_data_dir, *sub_dirs)
