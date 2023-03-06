from starlette.requests import Request
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context


async def index(request: Request):
    context = get_context(request)
    context["title"] = "Home"
    return templates.TemplateResponse('home.html', context)
