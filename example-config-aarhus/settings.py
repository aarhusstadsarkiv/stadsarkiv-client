import typing


settings: dict[str, typing.Any] = {
    "language": "da",
    "log_handlers": ["stream"],  # [ "stream", "file"]
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
        {"name": "page_images", "title": "Hjemmesider med billeder fra Aarhus", "template": "pages/images.html", "url": "/images"},
        {"name": "page_council", "title": "Aarhus Byråds arkiv", "template": "pages/council.html", "url": "/city-council"},
        {"name": "page_privacy", "title": "Privatlivspolitik", "template": "pages/about/privacy.html", "url": "/about/privacy"},
        {"name": "page_usability", "title": "Brugbarhed ", "template": "pages/about/usability.html", "url": "/about/usability"},
        {"name": "page_collections", "title": "Om samlingerne", "template": "pages/about/collections.html", "url": "/about/collections"},
        {"name": "page_availability", "title": "Tilgængelighed", "template": "pages/about/availability.html", "url": "/about/availability"},
        {
            "name": "page_archival_availability",
            "title": "Arkivlovens tilgængelighedsfrister",
            "template": "pages/about/archival_availability.html",
            "url": "/about/archival_availability",
        },
        {"name": "page_genealogy", "title": "Slægtsforskning", "template": "pages/guides/genealogy.html", "url": "/guides/genealogy"},
        {
            "name": "page_searchguide",
            "title": "Hjælp til søgning",
            "template": "pages/guides/searchguide.html",
            "url": "/guides/searchguide",
        },
        {
            "name": "page_municipality_records",
            "title": "Kommunearkivet ",
            "template": "pages/guides/municipality_records.html",
            "url": "/guides/municipality_records",
        },
        # /guides/genealogy
    ],
    "search_base_url": "/search",
}
