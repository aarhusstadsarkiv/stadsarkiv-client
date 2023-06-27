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
    "api_base_url": "https://dev.openaws.dk/v1",
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
        "Relationer": ["organisations", "locations", "events", "people", "objects"],
        "Rettighedsnoter": ["rights_notes"],
        "Anden juridisk beskyttelse": ["contractual_status_normalized", "other_legal_restrictions_normalized"],
        "Tilgængelighed": ["availability_normalized"],
        "Bestilling": ["ordering"],
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
    "record_definitions": {
        "last_updated": {"type": "date"},
        "date_normalized": {"type": "string"},
        "collectors": {"type": "link_list"},
        "locations": {"type": "link_list"},
        "potrait": {"type": "link"},
        "series": {"type": "link_list_hierarchy"},
        "desc_data": {"type": "key_value_dicts"},
        "availability": {"type": "label_dict"},
        "contractual_status_normalized": {"type": "string"},
        "other_legal_restrictions_normalized": {"type": "string"},
        "availability_normalized": {"type": "string"},
        "registration_id": {"type": "string"},
        "date_from": {"type": "string"},
        "content_types": {"type": "link_list_hierarchy"},
        "created_by": {"type": "string"},
        "id": {"type": "string"},
        "other_legal_restrictions": {"type": "label_dict"},
        "subjects": {"type": "link_list_hierarchy"},
        "admin_data": {"type": "key_value_dicts"},
        "type": {"type": "string"},
        "rights_notes": {"type": "string"},
        "admin_notes": {"type": "string"},
        "thumbnail": {"type": "url"},
        "resources": {"type": "key_value_dicts"},
        "schema": {"type": "string"},
        "curators": {"type": "link_list"},
        "copyright_status": {"type": "label_dict"},
        "copyright_status_normalized": {"type": "string_list"},
        "collection": {"type": "link_dict"},
        "last_updated_by": {"type": "string"},
        "original_id": {"type": "string"},
        "date_to": {"type": "string"},
        "representations": {"type": "representations"},  # special type
        "collection_tags": {"type": "link_list_hierarchy"},
        "created": {"type": "date"},
        "summary": {"type": "string"},
        "usability": {"type": "label_dict"},
        "organisations": {"type": "link_list"},
        "people": {"type": "link_list"},
        "objects": {"type": "link_list"},
        "events": {"type": "link_list"},
        "ordering": {"type": "ordering"},
        "creators": {"type": "link_list"},
        "desc_notes": {"type": "string"},
        "heading": {"type": "string"},
    },
}
