from typing import Any
from starlette.requests import Request
from stadsarkiv_client.core.flash import get_messages
from stadsarkiv_client.core import dynamic_settings
from stadsarkiv_client.hooks.manager import get_plugin_manager
from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log


log = get_log()
pm = get_plugin_manager()


async def _get_main_menu(request: Request):
    logged_in = await api.is_logged_in(request)
    permissions_list = await api.me_permissions(request)

    main_menu: Any = []  # type: ignore
    if "main_menu" in dynamic_settings.settings:
        main_menu = dynamic_settings.settings["main_menu"]  # type ignore

    if logged_in:
        main_menu = [item for item in main_menu if item["name"] != "login"]
        main_menu = [item for item in main_menu if item["name"] != "register"]
        main_menu = [item for item in main_menu if item["name"] != "forgot_password"]

    if not logged_in:
        main_menu = [item for item in main_menu if item["name"] != "logout"]
        main_menu = [item for item in main_menu if item["name"] != "profile"]

    if "admin" not in permissions_list:
        main_menu = [item for item in main_menu if item["name"] != "schemas"]
        main_menu = [item for item in main_menu if item["name"] != "entities"]

    return main_menu


def get_title(request: Request) -> str:
    pages: Any = []
    title = "No title"
    if "pages" in dynamic_settings.settings:
        pages = dynamic_settings.settings["pages"]

    for page in pages:
        if page["url"] == request.url.path:
            title = page["title"]
    return title


async def get_context(request: Request, context_values: dict = {}) -> dict:
    logged_in = await api.is_logged_in(request)
    context = {
        "path": request.url.path,
        "request": request,
        "title": get_title(request),
        "flash_messages": get_messages(request),
        "main_menu": await _get_main_menu(request),
        "logged_in": logged_in,
    }

    context.update(context_values)

    pm.hook.alter_context(context=context)  # type: ignore

    return context
