from starlette.requests import Request

from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.core import user

log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["admin"])
async def users_get(request: Request):
    users = await api.users_get(request)

    for user_ in users:
        permissions = user.permissions_as_list(user_["permissions"])
        permission_translated = user.permission_translated(permissions)
        user_["permission_translated"] = permission_translated

    context_values = {"title": "Brugere", "users": users}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("admin/users.html", context)