import typing


settings: dict[str, typing.Any] = {
    "client_name": "aarhusarkivet",
    "client_url": "https://aarhusarkivet.openaws.dk",
    "language": "da",
    "log_handlers": ["rotating_file"],  # ["stream"]
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": True,
        "secure": True,
        "samesite": "lax",
    },
    "api_base_url": "https://api.openaws.dk/v1",
    "main_menu": [
        {"name": "auth_login_get", "title": "Log ind", "type": "dropdown"},
        {"name": "auth_logout_get", "title": "Log ud", "type": "dropdown"},
        {"name": "auth_register_get", "title": "Ny bruger", "type": "dropdown"},
        {"name": "auth_me_get", "title": "Profil", "type": "dropdown"},
        {"name": "admin_users_get", "title": "Brugere", "type": "dropdown"},
        {"name": "schemas_get_list", "title": "Skemaer", "type": "dropdown"},
        {"name": "entities_get_list", "title": "Entiteter", "type": "dropdown"},
        {"name": "search_get", "title": "Søg", "type": "top"},
    ],
    "robots_allow": False,
    "allow_user_registration": True,
    "allow_user_management": True,
    "allow_online_ordering": True,
    "allow_bookmarks": True,
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
    {"name": "page_images", "title": "Hjemmesider med billeder fra Aarhus", "template": "pages/images.html", "url": "/images"},
    {"name": "page_council", "title": "Aarhus Byråds arkiv", "template": "pages/council.html", "url": "/city-council"},
]

pages_guides: list = [
    {
        "name": "page_searchguide",
        "title": "Hjælp til søgning",
        "template": "pages/guides/searchguide.html",
        "url": "/guides/searchguide",
        "type": "dropdown",
    },
    {
        "name": "page_genealogy",
        "title": "Slægtsforskning",
        "template": "pages/guides/genealogy.html",
        "url": "/guides/genealogy",
        "type": "dropdown",
    },
    {
        "name": "page_municipality_records",
        "title": "Kommunearkivet",
        "template": "pages/guides/municipality_records.html",
        "url": "/guides/municipality_records",
        "type": "dropdown",
    },
]

pages_about: list = [
    {
        "name": "page_collections",
        "title": "Om samlingerne",
        "template": "pages/about/collections.html",
        "url": "/about/collections",
        "type": "dropdown",
    },
    {
        "name": "page_availability",
        "title": "Tilgængelighed",
        "template": "pages/about/availability.html",
        "url": "/about/availability",
        "type": "dropdown",
    },
    {
        "name": "page_archival_availability",
        "title": "Arkivlovens tilgængelighedsfrister",
        "template": "pages/about/archival_availability.html",
        "url": "/about/archival_availability",
        "type": "dropdown",
    },
    {
        "name": "page_usability",
        "title": "Brugbarhed ",
        "template": "pages/about/usability.html",
        "url": "/about/usability",
        "type": "dropdown",
    },
    {
        "name": "page_privacy",
        "title": "Privatlivspolitik",
        "template": "pages/about/privacy.html",
        "url": "/about/privacy",
        "type": "dropdown",
    },
]

settings["pages"] = pages + pages_guides + pages_about

settings["main_menu_sections"] = [
    {"name": "guides", "title": "Vejledninger", "pages": pages_guides},
    {"name": "about", "title": "Om samlingerne", "pages": pages_about},
]
