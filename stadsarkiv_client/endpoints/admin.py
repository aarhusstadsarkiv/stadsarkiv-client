from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.auth import is_authenticated
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.core import user
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
import asyncio

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

    single_user, used_permissions = await asyncio.gather(
        api.user_get(request),
        api.user_permissions_subset(request),
    )

    permissions_user = user.permissions_as_list(single_user["permissions"])
    permission_translated = user.permission_translated(permissions_user)
    single_user["permission_translated"] = permission_translated

    context_values = {"title": "Bruger", "user": single_user, "permissions": used_permissions}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "admin/user_update.html", context)


async def users_patch(request: Request):
    uuid = request.path_params.get("uuid")
    redirect_url = request.url_for("admin_users_get_single", uuid=uuid)

    try:
        await is_authenticated(request, permissions=["root"])
        await api.users_patch(request)
        flash.set_message(request, translate("User has been updated"), type="success")
        return RedirectResponse(url=redirect_url, status_code=302)

    except Exception as e:
        log.exception(e)
        flash.set_message(request, translate("User could not be updated."), type="error")
        return RedirectResponse(url=redirect_url, status_code=302)


async def users_get_json(request: Request):
    await is_authenticated(request, permissions=["root"])
    user_ = await api.user_get(request)
    return JSONResponse(user_)


async def config_get(request: Request):
    await is_authenticated(request, permissions=["root"])
    dynamic_settings = settings
    return JSONResponse(dynamic_settings)
