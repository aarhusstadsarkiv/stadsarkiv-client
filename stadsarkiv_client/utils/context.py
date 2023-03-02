from starlette.requests import Request
from .flash import get_messages
from stadsarkiv_client.utils import dynamic_settings


def get_main_menu(request: Request) -> list:
    main_menu = []
    if "main_menu" in dynamic_settings.settings:
        main_menu = dynamic_settings.settings["main_menu"]

    if "logged_in" in request.session:
        main_menu = [x for x in main_menu if x["name"] != "login"]
        main_menu = [x for x in main_menu if x["name"] != "register"]

    if "logged_in" not in request.session:
        main_menu = [x for x in main_menu if x["name"] != "logout"]
        main_menu = [x for x in main_menu if x["name"] != "profile"]

    return main_menu


def get_title(request: Request) -> str:
    pages = []
    title = "No title"
    if "pages" in dynamic_settings.settings:
        pages = dynamic_settings.settings["pages"]

    for page in pages:
        if page["url"] == request.url.path:
            title = page["title"]
    return title


def logged_in(request: Request) -> bool:
    logged_in = False
    if "logged_in" in request.session:
        if request.session["logged_in"]:
            logged_in = True
    return logged_in


def get_context(request: Request) -> dict:
    dict_values = {
        'path': request.url.path,
        'request': request,
        'title': get_title(request),
        'flash_messages': get_messages(request),
        'main_menu': get_main_menu(request),
        'logged_in': logged_in(request),
    }

    return dict_values
