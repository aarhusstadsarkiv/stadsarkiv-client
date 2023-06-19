settings = {
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
    "fastapi_endpoint": "https://dev.openaws.dk",
    #
    # Main menu containing built-in endpoints, but you may remove these and generate your own menu.
    # You may also add other "menus", e.g. "footer_items" or something similar.
    #
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
}
