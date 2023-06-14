import logging
import os
from stadsarkiv_client.core.dotenv_local import load

load()


log_level = logging.DEBUG
cookie_httponly = False
cookie_secure = False
debug = True

if os.getenv("ENVIRONMENT") == "production":
    log_level = logging.INFO
    cookie_httponly = True
    cookie_secure = True
    debug = False

settings = {
    "debug": debug,
    "version": "0.0.1",
    "language": "da",
    "environment": os.getenv("ENVIRONMENT"),
    "log_level": log_level,
    "log_handlers": ["stream"],  # [ "stream", "file"]
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": cookie_httponly,
        "secure": cookie_secure,
        "samesite": "lax",
    },
    "fastapi_endpoint": "https://dev.openaws.dk",
    "main_menu": [
        {"name": "home", "title": "Hjem"},
        {"name": "login", "title": "Log ind"},
        {"name": "forgot_password", "title": "Glemt password"},
        {"name": "logout", "title": "Log ud"},
        {"name": "register", "title": "Ny bruger"},
        {"name": "profile", "title": "Profil"},
        {"name": "schemas", "title": "Schemas"},
        {"name": "entities", "title": "Entities"},
        {"name": "entities_search", "title": "Søg"},
        {"name": "records_search", "title": "Søg (som eksisterende aarhusarkiv)"},
    ],
    "pages": [
        {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
    ],
}
