from starlette.requests import Request

from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api

log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def users_get(request: Request):
    users = await api.users_get(request)

    context_values = {"title": "Brugere", "users": users}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("admin/users.html", context)
