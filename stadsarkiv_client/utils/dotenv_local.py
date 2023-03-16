from dotenv import load_dotenv
import sys
import os
from .logging_defs import get_init_logger

sys.path.append(".")
log = get_init_logger()


def load():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    env_dist = dir_path + "/.env-dist"
    load_dotenv(env_dist)

    # file exists
    if os.path.exists(".env"):
        log.info("Loaded local .env file")
        load_dotenv(override=True)
    else:
        log.info("Local .env file NOT loaded")


__ALL__ = ["load"]
