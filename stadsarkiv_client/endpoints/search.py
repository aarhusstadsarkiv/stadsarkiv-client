from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.hooks.manager import get_plugin_manager


pm = get_plugin_manager()
log = get_log()


async def get_search(request: Request):
    context_values = {"title": translate("Search")}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse("search/search.html", context)


async def get_search_results(request: Request):
    context_values = {"title": translate("Search")}
    context = await get_context(request, context_values=context_values)

    # query_params = pm.hook.alter_search(request=request)
    return templates.TemplateResponse("search/search-results.html", context)
