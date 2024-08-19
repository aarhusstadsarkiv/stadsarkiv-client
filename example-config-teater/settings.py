import typing


settings: dict[str, typing.Any] = {
    # test
    "client_name": "teaterarkivet",
    "client_url": "https://teater.openaws.dk",
    "language": "da",
    "log_handlers": ["rotating_file"],
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
    "api_base_url": "https://api.openaws.dk/v1",
    #
    # Main menu containing built-in endpoints, but you may remove these and generate your own menu.
    # You may also add other "menus", e.g. "footer_items" or something similar.
    #
    "main_menu": [
        # {"name": "auth_login_get", "title": "Log ind", "type": "dropdown"},
        {"name": "auth_logout_get", "title": "Log ud", "type": "overlay"},
        # {"name": "auth_register_get", "title": "Ny bruger", "type": "dropdown"},
        # {"name": "auth_me_get", "title": "Profil", "type": "dropdown"},
        # {"name": "admin_users_get", "title": "Brugere", "type": "dropdown"},
        # {"name": "schemas_get_list", "title": "Skemaer", "type": "dropdown"},
        # {"name": "entities_get_list", "title": "Entiteter", "type": "dropdown"},
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    "search_base_url": "/search",
    "search_keep_results": False,
    #
    # Allow robots
    #
    "show_version": True,
    "robots_allow": False,
    "facets_enabled": ["events"],
    "allow_user_registration": False,
    "allow_user_management": True,
    "allow_online_ordering": False,
    "ignore_record_keys": ["curators"],
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
    {"name": "home", "title": "Forside", "template": "pages/home.html", "url": "/"},
]

pages_guides: list = [
    {"name": "how_to_search", "title": "Søgevejledning", "template": "pages/how-to-search.html", "url": "/how-to-search"},
    {"name": "about_aarhus_teater", "title": "Om Aarhus Teaters Arkiv", "template": "pages/about.html", "url": "/about"},
    {"name": "practical_information", "title": "Praktisk Information", "template": "pages/info.html", "url": "/info"},
]

settings["pages"] = pages + pages_guides

settings["main_menu_sections"] = [
    {"name": "guides", "title": "Vejledninger", "pages": pages_guides},
]
