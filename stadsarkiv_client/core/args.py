"""
This file reads command line arguments that may be used in the application.
"""
import sys
import os
from stadsarkiv_client.core.logging_handlers import get_init_logger


log = get_init_logger()


def get_config_dir():
    """
    Get a config dir from command line arguments.
    If it is not set, return "local".
    If set check if it exists. If not just log a warning.
    """

    # add "--" to argument in order to find it in sys.argv
    argument = "--config-dir"
    if argument in sys.argv:
        index = sys.argv.index(argument)
        if len(sys.argv) > index + 1:
            config_dir = sys.argv[index + 1]

            # check if config_dir exists
            if os.path.exists(config_dir):
                return config_dir
            else:
                log.warn("Specified --config-dir does specified not exist: " + config_dir)

    return "local"
