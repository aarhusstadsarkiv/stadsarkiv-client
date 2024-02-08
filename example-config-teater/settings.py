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
    # "api_base_url": "http://localhost:8000/v1",
    "api_base_url": "https://dev.openaws.dk/v1",
    #
    # Main menu containing built-in endpoints, but you may remove these and generate your own menu.
    # You may also add other "menus", e.g. "footer_items" or something similar.
    #
    "main_menu": [
        {"name": "auth_login_get", "title": "Log ind", "type": "dropdown"},
        {"name": "auth_logout_get", "title": "Log ud", "type": "dropdown"},
        {"name": "auth_register_get", "title": "Ny bruger", "type": "dropdown"},
        {"name": "auth_me_get", "title": "Profil", "type": "dropdown"},
        {"name": "admin_users_get", "title": "Brugere", "type": "dropdown"},
        {"name": "schemas_get_list", "title": "Skemaer", "type": "dropdown"},
        {"name": "entities_get_list", "title": "Entiteter", "type": "dropdown"},
        {"name": "proxies_search_get", "title": "Søg", "type": "top"},
    ],
    "search_base_url": "/search",
    #
    # Allow robots
    #
    "robots_allow": True,
    "facets_enabled": ["events"],
}

# Custom pages
#
# "name" is the route name.
# "title" is the page title.
# "template" if the page you will use. It is also the content of the page.
# "url" is the path to the page
# "type" is the type of menu item. It can be "top" or "dropdown". If it is not set, it will not be displayed in the menu.
#
pages: list = [
    {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
    {"name": "how_to_search", "title": "Søgevejledning", "template": "pages/how-to-search.html", "url": "/how-to-search"},
    {"name": "about_aarhus_teater", "title": "Om Aarhus Teaters Arkiv", "template": "pages/about.html", "url": "/about"},
    {"name": "practical_information", "title": "Praktisk Information", "template": "pages/info.html", "url": "/info"},
]

settings["pages"] = pages

settings["main_menu_sections"] = []
