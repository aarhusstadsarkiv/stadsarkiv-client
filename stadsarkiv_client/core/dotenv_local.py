"""
load_dotenv wrapper
Load the module .env-dist file and override with local .env file if it exists
"""

from dotenv import load_dotenv
import os
from pathlib import Path
from stadsarkiv_client.core.logging_handlers import get_init_logger
from stadsarkiv_client.core.args import get_local_config_dir


log = get_init_logger()


def load():
    """
    Load the module .env-dist file
    Override with "local" .env file if it exists
    """
    dir_path = Path(__file__).resolve().parent.parent
    env_dist = dir_path / ".env.dist"
    load_dotenv(env_dist)
    log.info("Loaded .env.dist file")

    local_dot_env = get_local_config_dir(".env")

    if os.path.exists(local_dot_env):
        load_dotenv(local_dot_env, override=True)
        log.info(f"{local_dot_env} file loaded. Will override .env.dist settings")
    else:
        log.info(f"Local {local_dot_env} file NOT loaded")
