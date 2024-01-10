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
from stadsarkiv_client.core import cookie
import asyncio


log = get_log()


async def get_context(request: Request, context_values: dict = {}) -> dict:
    hooks = get_hooks(request)

    logged_in, permissions_list = await asyncio.gather(api.is_logged_in(request), api.me_permissions(request))

    # query_str_display is used to display the last search query
    # it is already present in the context_values if the client is requesting the search page
    if "query_str_display" not in context_values:
        context_values["query_str_display"] = cookie.get_query_str_display(request)

    context = {
        "permissions_list": permissions_list,
        "flash_messages": get_messages(request),
        "path": request.url.path,
        "request": request,
        "title": _get_title(request),
        "main_menu": await _get_main_menu(logged_in, permissions_list),
        "logged_in": logged_in,
    }

    context.update(context_values)

    if "meta_title" not in context:
        context["meta_title"] = context["title"]

    # Add context that applies to a single request to _context
    _context = context_values.copy()
    context["_context"] = _context

    context = await hooks.before_context(context=context)
    return context


async def _get_main_menu(logged_in: bool, permissions_list: list):
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
        main_menu = [item for item in main_menu if item["name"] != "admin_users_get"]
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
