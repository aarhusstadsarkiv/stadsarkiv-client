from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log


log = get_log()


async def get_page(request: Request) -> dict:
    pages = settings["pages"]
    page = next((item for item in pages if item["url"] == request.url.path), {})
    return page


async def default(request: Request):
    page = await get_page(request)

    log.debug(page)

    template = "pages/default.html"
    if "content" in page:
        template = page["content"]

    context_values = {"title": page["title"]}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(template, context)
