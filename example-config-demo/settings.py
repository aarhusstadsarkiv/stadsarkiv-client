import typing


settings: dict[str, typing.Any] = {
    "client_name": "development",
    "client_url": "https://client.openaws.dk",
    "language": "da",
    "log_handlers": ["rotating_file"],  # [ "stream", "file"]
    # "cors_allow_origins": ['https://client.openaws.dk'],
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": True,
        "secure": True,
        "samesite": "lax",
    },
    # "api_base_url": "http://localhost:8000/v1",
    "api_base_url": "https://dev.openaws.dk/v1",
    "main_menu": [
        {"name": "auth_login_get", "title": "Log ind", "type": "overlay"},
        {"name": "auth_logout_get", "title": "Log ud", "type": "overlay"},
        {"name": "auth_register_get", "title": "Ny bruger", "type": "overlay"},
        {"name": "auth_me_get", "title": "Profil", "type": "overlay"},
        {"name": "admin_users_get", "title": "Brugere", "type": "overlay"},
        {"name": "schemas_get_list", "title": "Skemaer", "type": "overlay"},
        {"name": "entities_get_list", "title": "Entiteter", "type": "overlay"},
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    "search_base_url": "/search",
    "robots_allow": False,
    "show_version": True,
    "allow_user_registration": True,
    "allow_user_management": True,
    "allow_online_ordering": True,
    "allow_bookmarks": True,
}
