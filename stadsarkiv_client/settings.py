import logging
import os
from stadsarkiv_client.core.dotenv_local import load
import typing

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
    "version": "0.0.4",
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
    "record_sections": {
        "Kernedata": ["collectors", "content_types", "creators", "date_normalized", "curators", "id"],
        "Beskrivelse": [
            "heading",
            "summary",
            "desc_notes",
            "collection",
            "series",
            "collection_tags",
            "subjects",
        ],
        "Ophavsret": ["copyright_status_normalized"],
        "Beskrivelsesdata": ["desc_data"],
        "Relationer": ["locations", "organisations", "events", "people", "objects"],
        "Rettighedsnoter": ["rights_notes"],
        "Anden juridisk beskyttelse": ["contractual_status_normalized", "other_legal_restrictions_normalized"],
        "Tilgængelighed": ["availability_normalized"],
        "Bestilling": ["ordering_normalized"],
        "Administration": [
            "admin_notes",
            "admin_data",
            "registration_id",
            "created_by",
            "created",
            "last_updated_by",
            "last_updated",
        ],
        "Resourcer": ["resources"],
        "Download": ["representations"],
    },
    "record_sections_employee": ["Administration", "Resourcer"],
}
