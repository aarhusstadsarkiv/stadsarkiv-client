from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.auth import is_authenticated
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.core import user
from stadsarkiv_client.core.dynamic_settings import settings

log = get_log()


async def users_get(request: Request):
    await is_authenticated(request, permissions=["root"])
    users = await api.users_get(request)

    for user_ in users:
        permissions = user.permissions_as_list(user_["permissions"])
        permission_translated = user.permission_translated(permissions)
        user_["permission_translated"] = permission_translated

    context_values = {"title": "Brugere", "users": users}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "admin/users.html", context)


async def _get_used_permissions(request: Request):
    """ "
    Only a subset of permissions are editable. This function returns the editable permissions.

    Permissions from endpoint is e.g.:
     [{'name': 'read', 'grant_id': 7, 'entity_id': None}, {'name': 'hard_delete', 'grant_id': 9, 'entity_id': None}]
    """
    permissions = await api.users_permissions(request)
    editable_permissions: list = ["guest", "user", "researcher", "admin", "employee", "root"]
    used_permissions = [p for p in permissions if p["name"] in editable_permissions]
    used_permissions = sorted(used_permissions, key=lambda x: x["grant_id"], reverse=False)
    return used_permissions


async def users_get_single(request: Request):
    await is_authenticated(request, permissions=["root"])

    user_ = await api.user_get(request)
    used_permissions = await _get_used_permissions(request)
    permissions_user = user.permissions_as_list(user_["permissions"])

    permission_translated = user.permission_translated(permissions_user)
    user_["permission_translated"] = permission_translated

    context_values = {"title": "Bruger", "user": user_, "permissions": used_permissions}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "admin/user_update.html", context)


async def users_get_json(request: Request):
    await is_authenticated(request, permissions=["root"])
    user_ = await api.user_get(request)
    return JSONResponse(user_)


async def config_get(request: Request):
    await is_authenticated(request, permissions=["root"])
    dynamic_settings = settings
    return JSONResponse(dynamic_settings)
