import typing


settings: dict[str, typing.Any] = {
    "language": "da",
    "log_handlers": ["stream", "rotating_file"],  # [ "stream", "file"]
    #
    # cookie settings
    #
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": True,
        "secure": True,
        "samesite": "lax",
    },
    "api_base_url": "https://dev.openaws.dk/v1",
    #
    # Main menu containing built-in endpoints, but you may remove these and generate your own menu.
    # You may also add other "menus", e.g. "footer_items" or something similar.
    #
    "main_menu": [
        {"name": "auth_login_get", "title": "Log ind"},
        {"name": "auth_forgot_password_get", "title": "Glemt password"},
        {"name": "auth_logout_get", "title": "Log ud"},
        {"name": "auth_register_get", "title": "Ny bruger"},
        {"name": "auth_me_get", "title": "Profil"},
        {"name": "schemas_get_list", "title": "Schemas"},
        {"name": "entities_get_list", "title": "Entities"},
        {"name": "records_search_get", "title": "Søg"},
    ],
    #
    # Custom pages
    #
    # "name" is the route name. Title is the page title.
    # "template" if the page you will use. It is also the content of the page.
    # "url" is the path to the page
    #
    # You can then make another menu which contains some of these pages, e.g. a "footer_items" entry
    # or something similar.
    "pages": [
        {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
    ],
    # Which of the default facets should be enabled
    "facets_enabled": ["content_types", "events", "dates"],
}
