import logging
import os

from dotenv import load_dotenv

dir_path = os.path.dirname(os.path.realpath(__file__))
env_dist = dir_path + "/.env-dist"
load_dotenv(env_dist)
load_dotenv(override=True)


log_level = logging.DEBUG
cookie_httponly = False
cookie_secure = False
fastapi_endpoint = "https://dev.openaws.dk"


if os.getenv("ENVIRONMENT") == "production":
    log_level = logging.INFO
    cookie_httponly = True
    cookie_secure = True
    fastapi_endpoint = "https://dev.openaws.dk"


settings = {

    "environment": os.getenv("ENVIRONMENT"),
    "fastapi_endpoint": fastapi_endpoint,
    "log_level": log_level,
    # "file" or "stream" or both
    # "file" will log to ./logs/main.log
    "log_handlers": ["stream"],
    "cookie": {
        "name": "session",
        "lifetime": 3600 * 24 * 14,
        "httponly": cookie_httponly,
        "secure": cookie_secure,
        "samesite": "lax"
    }
}


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/templates"
if os.path.exists(dir_path):
    settings["templates_local"] = dir_path
