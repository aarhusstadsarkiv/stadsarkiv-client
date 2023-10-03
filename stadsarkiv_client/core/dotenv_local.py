"""
load_dotenv wrapper
Load the module .env-dist file and override with local .env file if it exists
"""

from dotenv import load_dotenv
import sys
import os
from stadsarkiv_client.core.logging_handlers import get_init_logger
from stadsarkiv_client.core.args import get_config_dir


sys.path.append(".")
log = get_init_logger()


def load():
    """
    Load the module .env-dist file
    Override with "local" .env file if it exists
    """
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    env_dist = dir_path + "/.env-dist"
    load_dotenv(env_dist)
    log.debug("Loaded .env-dist file")

    local_config_dir = get_config_dir()
    local_dot_env = f"{local_config_dir}/.env"

    if os.path.exists(local_dot_env):
        load_dotenv(local_dot_env, override=True)
        log.debug(f"{local_dot_env} file loaded. Will override .env-dist settings")
    else:
        log.debug(f"Local {local_dot_env} file NOT loaded")
