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
    # pages
    # "name" is the route name. Title is the page title.
    # "template" if the page you will use. It is also the content of the page.
    # "url" is the path to the page
    "pages": [
        {"name": "home", "title": "Hjem", "template": "pages/home.html", "url": "/"},
        {"name": "page_searchguide", "title": "Hjælp til søgning", "template": "pages/searchguide.html", "url": "/guides/searchguide"},
        {"name": "page_collections", "title": "Om samlingerne", "template": "pages/collections.html", "url": "/about/collections"},
    ],
    # Top menu items. These are the default items. You may remove or add more.
    # The "type" can be "icon" or "text".
    "main_menu_top": [
        {"name": "search_get", "title": "Søg", "type": "icon", "icon": "search"},
    ],
    # Main menu system contains built-in endpoints. You may remove some of these.
    #
    "main_menu_system": [
        {"name": "auth_login_get", "title": "Log ind"},
        {"name": "auth_logout_get", "title": "Log ud"},
        {"name": "auth_register_get", "title": "Ny bruger"},
        {"name": "auth_me_get", "title": "Profil"},
        {"name": "admin_users_get", "title": "Brugere"},
        {"name": "schemas_get_list", "title": "Skemaer"},
        {"name": "entities_get_list", "title": "Entiteter"},
    ],
    # Main menu sections
    # Custom pages can be added to the main menu sections
    "main_menu_sections": [
        {
            "name": "guides",
            "title": "Vejledninger",
            "pages": [
                {
                    "name": "page_searchguide",
                    "title": "Hjælp til søgning",
                },
            ],
        },
        {
            "name": "about",
            "title": "Om samlingerne",
            "pages": [
                {
                    "name": "page_collections",
                    "title": "Om samlingerne",
                },
            ],
        },
    ],
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
