import logging
import os
from stadsarkiv_client.core.dotenv_local import load

load()


log_level = logging.DEBUG
cookie_httponly = False
cookie_secure = False


if os.getenv("ENVIRONMENT") == "production":
    log_level = logging.INFO
    cookie_httponly = True
    cookie_secure = True


settings = {
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
    "fastapi_endpoint": "http://localhost:8000",
    "main_menu": [
        {"name": "home", "title": "Hjem"},
        {"name": "about", "title": "Om"},
        {"name": "login", "title": "Log ind"},
        {"name": "logout", "title": "Log ud"},
        {"name": "register", "title": "Ny bruger"},
        {"name": "profile", "title": "Profil"},
        {"name": "schemas", "title": "Schemas"},
        {"name": "entities", "title": "Entities"},
        {"name": "entities_search", "title": "Søg Entities"},
        {"name": "records", "title": "Records"},
    ],
    "pages": [
        {"name": "home", "title": "Hjem", "page": "pages/home.html", "url": "/"},
        {"name": "about", "title": "Om", "page": "pages/about.html", "url": "/about"},
    ],
}
