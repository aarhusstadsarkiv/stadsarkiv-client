from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from urllib.parse import quote_plus

log = get_log()


async def get_params_as_tuple_list(request: Request, remove_keys=[]):
    query_params = request.query_params
    items = query_params.multi_items()
    items = [(key, value) for key, value in items if key not in remove_keys]
    return items


async def get_params_as_query_str(request: Request, remove_keys=[]):
    """Get query params from request and return it as a encoded string."""

    items = await get_params_as_tuple_list(request, remove_keys=remove_keys)
    query_str = ""
    for key, value in items:
        query_str += f"{key}={quote_plus(value)}&"

    return query_str


async def get_search_query(request: Request):
    """Get search query "q" from request and return it as a string."""
    query_params = request.query_params
    q = query_params.get("q", "")
    return q
