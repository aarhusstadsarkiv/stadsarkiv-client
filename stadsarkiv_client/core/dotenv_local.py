from dotenv import load_dotenv
import sys
import os
from stadsarkiv_client.core.logging_defs import get_init_logger

sys.path.append(".")
log = get_init_logger()


def load():
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    env_dist = dir_path + "/.env-dist"
    load_dotenv(env_dist)
    log.debug("Loaded .env-dist file")

    if os.path.exists(".env"):
        load_dotenv(override=True)
        log.debug("Local .env file loaded. Will override .env-dist settings")
    else:
        log.debug("Local .env file NOT loaded")
