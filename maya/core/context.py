"""
This module provides helper functions to construct the context dictionary used in rendering templates
within the Maya application. It integrates user session data, permissions, settings-based menus, and
hook-based extensibility into a unified structure for use in frontend views.

Functions included:
- `get_context`: Builds the complete context dictionary, incorporating request-specific and global data.
- `_generate_menu_urls`: Generates URLs for menu items, handling query strings and login redirection.
- `_get_main_menu_system`: Filters system menu items based on user authentication state and permissions.
- `_get_title`: Retrieves the page title based on the request URL from the configuration.
- `_get_authorization`: Provides an authorization header if the user is logged in.

The module relies on internal APIs, dynamic settings, and cookie/session utilities to maintain
a consistent user interface and behavior across pages.
"""

from starlette.requests import Request
from maya.core.flash import get_messages
from maya.core.dynamic_settings import settings
from maya.core import api
from maya.core.hooks import get_hooks
from maya.core import cookie
from maya.core.logging import get_log
import urllib.parse

log = get_log()


async def get_context(request: Request, context_values: dict = {}, identifier: str = "") -> dict:
    """
    This function is used to get the context for the templates.
    `context_values` is a dict that can be used to pass additional context values to the templates.
    `identifier` is a string that can be used to identify the context.
    """
    hooks = get_hooks(request)

    logged_in = await api.is_logged_in(request)
    permissions_list = await api.me_permissions(request)
    current_path = request.url.path

    # query_str_display is used to display the last search query
    # it is already present in the context_values if the client is requesting the search page
    # if it is not present, we need to add it to the context_values
    query_str_display = context_values.get("query_str_display", "")
    if "query_str_display" not in context_values:
        query_str_display = cookie.get_query_str_display(request)

    main_menu_system = _get_main_menu_system(logged_in, permissions_list)
    main_menu_system = _generate_menu_urls(request, main_menu_system, query_str_display, current_path)
    main_menu_top = _generate_menu_urls(request, settings["main_menu_top"], query_str_display, current_path)

    context = {
        "query_str_display": query_str_display,
        "identifier": identifier,
        "permissions_list": permissions_list,
        "flash_messages": get_messages(request),
        "current_path": request.url.path,
        "request": request,
        "title": _get_title(request),
        "main_menu_top": main_menu_top,
        "main_menu_system": main_menu_system,
        "main_menu_sections": settings["main_menu_sections"],
        "logged_in": logged_in,
        "authorization": _get_authorization(request),
        "dark_theme": request.cookies.get("dark_theme", False),
    }

    # Add context_values to context
    context.update(context_values)

    if "meta_title" not in context:
        context["meta_title"] = context["title"]

    if "meta_description" not in context:
        context["meta_description"] = context["meta_title"]

    context = await hooks.before_context(context=context)
    return context


def _generate_menu_urls(request: Request, menu_items: list, query_str_display: str, current_path=None):
    """
    Generate URLs for the main menu items.
    In order to ease the process of using the items in the frontend.
    """
    for menu_item in menu_items:
        url = str(request.url_for(menu_item["name"]))
        if menu_item["name"] == "search_get":

            # Add query_str_display to search url
            menu_item["url"] = f"{url}?{query_str_display}"
        elif menu_item["name"] == "auth_login_get" and current_path:

            # Add next parameter to login url
            current_path = request.url.path
            if request.query_params:
                current_path += f"?{request.query_params}"

            next_url = urllib.parse.quote(current_path, safe="")
            menu_item["url"] = f"{url}?next={next_url}"
        else:
            menu_item["url"] = url

    return menu_items


def _get_main_menu_system(logged_in: bool, permissions_list: list) -> list:
    """
    Get the main menu system. Based on the settings and the user's permissions.
    """
    main_menu_system: list = settings["main_menu_system"]

    if not settings.get("allow_user_registration", False):
        excluded_items = {
            "auth_login_get",
            "auth_register_get",
            "auth_forgot_password_get",
            "auth_logout_get",
            "auth_me_get",
            "auth_register_post",
            "auth_login_post",
            "auth_forgot_password_post",
        }
        main_menu_system = [item for item in main_menu_system if item["name"] not in excluded_items]

    if logged_in:
        excluded_items = {"auth_login_get", "auth_register_get", "auth_forgot_password_get"}
        main_menu_system = [item for item in main_menu_system if item["name"] not in excluded_items]

    if not logged_in:
        excluded_items = {"auth_logout_get", "auth_me_get"}
        main_menu_system = [item for item in main_menu_system if item["name"] not in excluded_items]

    if "employee" not in permissions_list:
        excluded_items = {"orders_admin_get"}
        main_menu_system = [item for item in main_menu_system if item["name"] not in excluded_items]

    if "root" not in permissions_list and "admin" not in permissions_list:
        excluded_items = {"admin_users_get", "schemas_get_list", "entities_get_list"}
        main_menu_system = [item for item in main_menu_system if item["name"] not in excluded_items]

    return main_menu_system


def _get_title(request: Request) -> str:
    """
    Get a title for a page which is part of settings["pages"].
    """

    title = ""
    pages: list[dict] = settings["pages"]

    for page in pages:
        if page["url"] == request.url.path:
            title = page["title"]
    return title


def _get_authorization(request: Request):
    """
    Add authorization header to context if user is logged in.
    This makes it possible to use the header in the frontend.
    E.g. to make requests to the API using javascript.
    """
    if "access_token" in request.session:
        token = request.session["access_token"]
        return f"Bearer {token}"

    return None
