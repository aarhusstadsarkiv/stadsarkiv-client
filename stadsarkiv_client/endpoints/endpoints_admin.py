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


async def admin_users_get(request: Request):
    await is_authenticated(request, permissions=["admin"])
    users = await api.users_get(request)

    for user_ in users:
        permissions = user.permissions_as_list(user_["permissions"])
        permission_translated = user.permission_translated(permissions)
        user_["permission_translated"] = permission_translated

    context_values = {"title": "Brugere", "users": users}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "admin/users.html", context)


async def admin_users_get_single(request: Request):
    await is_authenticated(request, permissions=["admin"])

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


async def admin_users_patch(request: Request):
    await is_authenticated(request, permissions=["admin"])

    uuid = request.path_params.get("uuid")
    redirect_url = request.url_for("admin_users_get_single", uuid=uuid)

    try:
        await api.users_patch_permissions(request)
        flash.set_message(request, translate("User has been updated"), type="success")
        return RedirectResponse(url=redirect_url, status_code=302)

    except Exception:
        log.exception("Error in admin_users_patch")
        flash.set_message(request, translate("User could not be updated."), type="error")
        return RedirectResponse(url=redirect_url, status_code=302)


async def admin_test(request: Request):
    pass
    # await is_authenticated(request, permissions=["admin"])

    # me = await api.me_get(request)

    # log.debug("me")
    # log.debug(me)

    # users = await api.users_get(request)
    # for user_ in users:
    #     id = user_["id"]
    #     email = user_["email"]
    #     log.debug(email)

    #     custom_data = UserData(user_)
    #     custom_data.set_custom_value("test", "test")

    #     custom_data.append_bookmark("111111222")
    #     data = custom_data.get_data()
    #     log.debug(data)

    #     new_data = await api.users_data_post(request, id=id, data=data)
    #     log.debug(new_data)
    # await api.users_patch_permissions(request)

    # log.debug(users)
    # return JSONResponse(users)


async def admin_users_get_json(request: Request):
    await is_authenticated(request, permissions=["admin"])
    user_ = await api.user_get(request)
    return JSONResponse(user_)


async def admin_config_get(request: Request):
    await is_authenticated(request, permissions=["admin"])
    dynamic_settings = settings
    return JSONResponse(dynamic_settings)
