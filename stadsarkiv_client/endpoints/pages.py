from starlette.requests import Request
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context


async def default(request: Request):

    context = get_context(request)
    return templates.TemplateResponse('pages/default.html', context)
