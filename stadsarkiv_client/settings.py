"""
Default settings for stadsarkiv_client
These settings can be overridden by creating a local settings file.
"""

import logging
import os
from stadsarkiv_client.core.dotenv_local import load
import typing
import stadsarkiv_client

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

settings: dict[str, typing.Any] = {
    "debug": debug,
    "robots_allow": False,
    "version": stadsarkiv_client.__version__,
    "show_version": True,
    "language": "da",
    "environment": os.getenv("ENVIRONMENT"),
    "log_level": log_level,
    "log_handlers": ["stream", "file"],
    "sentry_level": logging.INFO,
    "sentry_event_level": logging.WARNING,
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": cookie_httponly,
        "secure": cookie_secure,
        "samesite": "lax",
    },
    "custom_error": "Der skete en system fejl. Prøv igen lidt senere!",
    "api_base_url": "https://dev.openaws.dk/v1",
    "main_menu": [
        {"name": "login", "title": "Log ind"},
        {"name": "forgot_password", "title": "Glemt password"},
        {"name": "logout", "title": "Log ud"},
        {"name": "register", "title": "Ny bruger"},
        {"name": "profile", "title": "Profil"},
        {"name": "schemas", "title": "Schemas"},
        {"name": "entities", "title": "Entities"},
        {"name": "records_search", "title": "Søg"},
    ],
    "pages": [
        {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
    ],
    "search_base_url": "/search",
    "facets_enabled": ["content_types", "subjects", "availability", "usability", "dates"],
}
