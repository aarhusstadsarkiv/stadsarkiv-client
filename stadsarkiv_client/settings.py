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
    "version" : "0.0.1",
    "language": "da",
    "environment": os.getenv("ENVIRONMENT"),
    "fastapi_endpoint": fastapi_endpoint,
    "log_level": log_level,
    "log_handlers": ["stream"],  # [ "stream", "file"]
    "cookie": {
        "name": "session",
        "lifetime": 3600 * 24 * 14,
        "httponly": cookie_httponly,
        "secure": cookie_secure,
        "samesite": "lax"
    },
    "main_menu": [
        {
            "name": "home",
            "title": "Hjem"
        },
        {
            "name": "about",
            "title": "Om"
        },
        {
            "name": "login",
            "title": "Log ind"
        },
        {
            "name": "logout",
            "title": "Log ud"
        },
        {
            "name": "register",
            "title": "Register"
        },
        {
            "name": "profile",
            "title": "Profil"
        },

    ],
    "pages": [
        {
            "name": "home",
            "title": "Hjem",
            "page": "pages/home.html",
            "url": "/"
        },
        {
            "name": "about",
            "title": "Om",
            "page": "pages/about.html",
            "url": "/about"
        }
    ]
}
