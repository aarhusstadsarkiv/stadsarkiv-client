from starlette.requests import Request
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.hooks.manager import get_plugin_manager
from hooks import alter_search_query


pm = get_plugin_manager()
log = get_log()


async def get_search(request: Request):

    context_values = {"title": translate("Search")}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('search/search.html', context)


async def get_search_results(request: Request):

    context_values = {"title": translate("Search")}
    context = get_context(request, context_values=context_values)

    # query_params = pm.hook.alter_search(request=request)  # type: ignore
    # log.debug(query_params)
    # log.debug('query')

    query_params = alter_search_query(request)
    log.debug(query_params)
    
    return templates.TemplateResponse('search/search-results.html', context)


__ALL__ = [get_search]
