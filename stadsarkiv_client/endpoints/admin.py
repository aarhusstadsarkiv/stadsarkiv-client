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


async def users_get_single(request: Request):
    await is_authenticated(request, permissions=["root"])

    user_ = await api.user_get(request)
    permissions = await api.users_permissions(request)

    permissions_user = user.permissions_as_list(user_["permissions"])

    permission_translated = user.permission_translated(permissions_user)
    user_["permission_translated"] = permission_translated

    context_values = {"title": "Bruger", "user": user_, "permissions": permissions}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "admin/user_update.html", context)


async def config_get(request: Request):
    await is_authenticated(request, permissions=["root"])
    dynamic_settings = settings
    return JSONResponse(dynamic_settings)
