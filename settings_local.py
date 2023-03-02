settings_local = {
    "language": "da",
    # "language_local": "./language.py", # Override translations
    # "templates_local": "./templates",  # Override templates
    # "static_local": "./static",  # Override static folder
    "main_menu": [
        {
            "name": "home",
            "title": "Hjem"
        },
        {
            "name": "about",
            "title": "Om"
        },
        {
            "name": "login",
            "title": "Log ind"
        },
        {
            "name": "logout",
            "title": "Log ud"
        },
        {
            "name": "register",
            "title": "Register"
        },
        {
            "name": "profile",
            "title": "Profil"
        },

    ],
    "pages": [
        {
            "name": "home",
            "title": "Hjem",
            "page": "pages/home.html",
            "url": "/"
        },
        {
            "name": "about",
            "title": "Om",
            "page": "pages/about.html",
            "url": "/about"
        }
    ]
}
