"""
This file exposes 'get_base_dir_path' and 'get_data_dir_path' to the rest of the application.

The 'BASE_DIR' is required as argument to the Maya CLI. In this dir
it is expected that settings, logs, hooks, plugins, sqlite3 databases etc. exists.

It is then added to the environment when the server is started.

The get_data_dir() function will return the path to the data directory.
The data directory is a subdirectory of the base directory.

"""

import os


def get_base_dir_path(*sub_dirs: str) -> str:
    """
    Get a base dir path
    """
    # Get env BASE_DIR from os. This is set in the command line arguments to the server.
    base_dir = os.environ.get("BASE_DIR")

    # raise an error if the config dir is not set
    if base_dir is None:
        raise ValueError("BASE_DIR is not set. Please set it to a valid directory.")

    # join the sub_dirs to the local_config_dir
    paths = os.path.join(base_dir, *sub_dirs)

    return paths


def get_data_dir_path(*sub_dirs: str) -> str:
    """
    Get a data dir path
    """
    base_dir = get_base_dir_path()
    local_data_dir = os.path.join(base_dir, "data")

    return os.path.join(local_data_dir, *sub_dirs)
