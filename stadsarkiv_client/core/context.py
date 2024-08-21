"""
Contains a single function (get_context)
that returns a dict with basic context values for the templates.
Hooks: You are able to hook into the get_context function and add your own context values.
"""

from starlette.requests import Request
from stadsarkiv_client.core.flash import get_messages
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.core import cookie


log = get_log()


async def get_context(request: Request, context_values: dict = {}, identifier: str = "") -> dict:
    """
    Adding some default values to the context.
    """
    hooks = get_hooks(request)

    logged_in = await api.is_logged_in(request)
    permissions_list = await api.me_permissions(request)

    # query_str_display is used to display the last search query
    # it is already present in the context_values if the client is requesting the search page
    # if it is not present, we need to add it to the context_values
    if "query_str_display" not in context_values:
        context_values["query_str_display"] = cookie.get_query_str_display(request)

    context = {
        "identifier": identifier,
        "permissions_list": permissions_list,
        "flash_messages": get_messages(request),
        "path": request.url.path,
        "request": request,
        "title": _get_title(request),
        "main_menu_user": _get_main_menu_user(logged_in, permissions_list),
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

    # Add context that applies to a single request to _context
    _context = context_values.copy()
    context["_context"] = _context

    context = await hooks.before_context(context=context)
    return context


def _get_main_menu_user(logged_in: bool, permissions_list: list):
    main_menu: list = settings["main_menu"]

    if logged_in:
        excluded_items = {"auth_login_get", "auth_register_get", "auth_forgot_password_get"}
        main_menu = [item for item in main_menu if item["name"] not in excluded_items]

    if not logged_in:
        excluded_items = {"auth_logout_get", "auth_me_get"}
        main_menu = [item for item in main_menu if item["name"] not in excluded_items]

    if "root" not in permissions_list and "admin" not in permissions_list:
        excluded_items = {"admin_users_get", "schemas_get_list", "entities_get_list"}
        main_menu = [item for item in main_menu if item["name"] not in excluded_items]

    return main_menu


def _get_title(request: Request) -> str:
    """"
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
