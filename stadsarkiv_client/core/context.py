"""
Contains a single function (get_context)
that returns a dict with basic context values for the templates.
Hooks: You are able to hook into the get_context function and add your own context values.
"""

from typing import Any
from starlette.requests import Request
from stadsarkiv_client.core.flash import get_messages
from stadsarkiv_client.core import dynamic_settings
from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks import get_hooks


log = get_log()


async def get_context(request: Request, context_values: dict = {}) -> dict:
    hooks = get_hooks(request)
    logged_in = await api.is_logged_in(request)
    context = {
        "flash_messages": get_messages(request),
        "path": request.url.path,
        "request": request,
        "title": _get_title(request),
        "main_menu": await _get_main_menu(request),
        "logged_in": logged_in,
    }

    context.update(context_values)

    if "meta_title" not in context:
        context["meta_title"] = context["title"]

    # Add context that applies to a single request to _context
    _context = context_values.copy()
    context["_context"] = _context

    context = hooks.before_get_context(context=context)
    return context


async def _get_main_menu(request: Request):
    logged_in = await api.is_logged_in(request)
    permissions_list = await api.me_permissions(request)

    main_menu: Any = []
    if "main_menu" in dynamic_settings.settings:
        main_menu = dynamic_settings.settings["main_menu"]  # type ignore

    if logged_in:
        main_menu = [item for item in main_menu if item["name"] != "auth_login_get"]
        main_menu = [item for item in main_menu if item["name"] != "auth_register_get"]
        main_menu = [item for item in main_menu if item["name"] != "auth_forgot_password_get"]

    if not logged_in:
        main_menu = [item for item in main_menu if item["name"] != "auth_logout_get"]
        main_menu = [item for item in main_menu if item["name"] != "auth_me_get"]

    if "admin" not in permissions_list:
        main_menu = [item for item in main_menu if item["name"] != "schemas_get_list"]
        main_menu = [item for item in main_menu if item["name"] != "entities_get_list"]

    return main_menu


def _get_title(request: Request) -> str:
    pages: Any = []
    title = ""
    if "pages" in dynamic_settings.settings:
        pages = dynamic_settings.settings["pages"]

    for page in pages:
        if page["url"] == request.url.path:
            title = page["title"]
    return title
