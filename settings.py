settings = {
    "language": "da",
    "fastapi_endpoint": "http://localhost:8000/v1",
    "cookie": {
        "name": "session",
        "lifetime": 60,  # seconds
        "httponly": False,
        "secure": False,
        "samesite": "lax"
    },
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
            "title": "Ny bruger"
        },
        {
            "name": "profile",
            "title": "Profil"
        },
        {
            "name": "schemas",
            "title": "Schemas"
        },
        {
            "name": "search",
            "title": "Søg"
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
