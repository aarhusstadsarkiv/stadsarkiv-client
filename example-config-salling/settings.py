import typing


settings: dict[str, typing.Any] = {
    "client_name": "development",
    "client_url": "https://demo.openaws.dk",
    "client_email": "stadsarkivet@aarhusarkivet.dk",
    "language": "da",
    "log_handlers": ["rotating_file"],
    # "cors_allow_origins": ['https://demo.openaws.dk'],
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": True,
        "secure": True,
        "samesite": "lax",
    },
    # "api_base_url": "http://localhost:8000/v1",
    "api_base_url": "https://dev.openaws.dk/v1",
    "pages": [
        {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
        {"name": "about", "title": "Om SallingArkivet", "template": "pages/about.html", "url": "/om-sallingarkivet"},
        {"name": "privatlivspolitik", "title": "Privatlivspolitik", "template": "pages/privacy.html", "url": "/privatlivspolitik"},
    ],
    "main_menu_top": [
        {"name": "search_get", "title": "Udforsk Arkivet", "type": "text"},
        {"name": "stories", "title": "Fortællinger", "type": "text"},
        # {"name": "memories", "title": "Erindringer", "type": "text"},
        {"name": "about", "title": "Om Arkivet", "type": "text"},
        # {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    "main_menu_system": [],
    "sqlite3": {
        "default": "data/database.db",
        "orders": "data/orders.db",
    },
    "search_base_url": "/search",
    "show_version": True,
    "allow_user_registration": False,
    "allow_user_management": False,
    "allow_save_bookmarks": False,
    "allow_save_search": False,
    "allow_online_ordering": False,
    "ignore_record_keys": ["curators", "collectors", "collection", "organisations"],
}
