from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context


async def index(request: Request):
    context_values = {"title": "Home"}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("home.html", context)
