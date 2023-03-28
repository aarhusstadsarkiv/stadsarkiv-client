from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context


async def default(request: Request):
    context_values = {"title": "Default"}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("pages/default.html", context)
