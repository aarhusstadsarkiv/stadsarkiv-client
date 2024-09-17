import typing


settings: dict[str, typing.Any] = {
    # This should be the name of the client, e.g. "aarhusarkivet"
    #
    # If you are running in production, you should change this to the name of your client
    # If you are running in development, you can leave it as "development"
    "client_name": "development",
    # This should be the url of the client, e.g. "https://aarhusarkivet.openaws.dk"
    # If running on localhost you may change this to e.g. "http://localhost:5555"
    "client_url": "https://demo.openaws.dk",
    # If you are running in production, you may set this to True in order to allow robots to index the site
    "robots_allow": False,
    # show the version of the stadarkiv-client
    "show_version": True,
    # only supported language is "da" for now
    "language": "da",
    # log handlers can be "stream", "rotating_file"
    # on development you can use "stream" to see logs in the console
    "log_handlers": ["stream", "rotating_file"],  # [ "stream", "file", "rotating_file"]
    # cookie settings. These settings are reasonable defaults
    "cookie": {
        "name": "session",
        "lifetime": 3600,  # seconds
        "httponly": True,
        "secure": True,
        "samesite": "lax",
    },
    # Set a 500 custom error message
    "custom_error": "Der skete en system fejl. Prøv igen lidt senere!",
    # Is you are running in production, you should change the api_base_url to the production API.
    # production "api_base_url": "https://api.openaws.dk/v1",
    "api_base_url": "https://dev.openaws.dk/v1",
    # Main menu containing built-in endpoints, but you may remove these and generate your own menu.
    # You may also add other "menus", e.g. "footer_items" or something similar.
    #
    "main_menu_system": [
        {"name": "auth_login_get", "title": "Log ind", "type": "overlay"},
        {"name": "auth_logout_get", "title": "Log ud", "type": "overlay"},
        {"name": "auth_register_get", "title": "Ny bruger", "type": "overlay"},
        {"name": "auth_me_get", "title": "Profil", "type": "overlay"},
        {"name": "admin_users_get", "title": "Brugere", "type": "overlay"},
        {"name": "schemas_get_list", "title": "Skemaer", "type": "overlay"},
        {"name": "entities_get_list", "title": "Entiteter", "type": "overlay"},
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    # There is another "type of menu" which is "text" that is a simple text link, e.g.:
    # {"name": "auth_login_get", "title": "Log ind", "type": "text"},
    # The facets enabled in the search
    # These are the defaults: ["content_types", "subjects", "availability", "usability", "dates"]
    # The facets are loaded from 'settings_facets.py'
    "facets_enabled": ["content_types", "events", "dates"],
    # CORS allow origins
    "cors_allow_origins": [],
    # Allow user registration
    "allow_user_registration": True,
    # Allow user management
    "allow_user_management": True,
    # Allow online ordering
    "allow_online_ordering": False,
    # Ignore record keys so that the will not be displayed in the record template
    "ignore_record_keys": [],
    # keep search result from last search when navigating to other pages
    "search_keep_results": True,
}

# pages
#
# "name" is the route name. Title is the page title.
# "template" if the page you will use. It is also the content of the page.
# "url" is the path to the page
# "type" is the type of menu item. It can be "top" or "overlay".
#  If it is not set, it will not be displayed in the top bar menu.

pages: list = [
    {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
]

pages_guides: list = [
    {
        "name": "page_searchguide",
        "title": "Hjælp til søgning",
        "template": "pages/searchguide.html",
        "url": "/guides/searchguide",
        "type": "overlay",
    },
]

pages_about: list = [
    {
        "name": "page_collections",
        "title": "Om samlingerne",
        "template": "pages/collections.html",
        "url": "/about/collections",
        "type": "overlay",
    },
]

settings["pages"] = pages + pages_guides + pages_about

# Add pages as sections in the main menu
settings["main_menu_sections"] = [
    {"name": "guides", "title": "Vejledninger", "pages": pages_guides},
    {"name": "about", "title": "Om samlingerne", "pages": pages_about},
]
