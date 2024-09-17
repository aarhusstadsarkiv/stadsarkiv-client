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
    "client_name": "development",
    "client_url": "https://demo.openaws.dk",
    "debug": debug,
    "robots_allow": False,
    "version": stadsarkiv_client.__version__,
    "show_version": True,
    "language": "da",
    "environment": os.getenv("ENVIRONMENT"),
    "log_level": log_level,
    "log_handlers": ["stream", "rotating_file"],
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
    "main_menu_top": [
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    "main_menu_system": [
        {"name": "auth_login_get", "title": "Log ind"},
        {"name": "auth_logout_get", "title": "Log ud"},
        {"name": "auth_register_get", "title": "Ny bruger"},
        {"name": "auth_me_get", "title": "Profil"},
        {"name": "admin_users_get", "title": "Brugere"},
        {"name": "schemas_get_list", "title": "Skemaer"},
        {"name": "entities_get_list", "title": "Entiteter"},
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    "main_menu_sections": [],
    "search_base_url": "/search",
    "search_keep_results": True,
    "facets_enabled": ["content_types", "subjects", "availability", "usability", "dates"],
    "cors_allow_origins": [],
    "allow_user_registration": True,
    "allow_user_management": True,
    "allow_online_ordering": False,
    "allow_save_bookmarks": False,
    "ignore_record_keys": [],
}

pages: list = [{"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"}]

settings["pages"] = pages
