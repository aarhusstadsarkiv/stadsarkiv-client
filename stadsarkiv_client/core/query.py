from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from urllib.parse import quote_plus

log = get_log()


async def get_list(request: Request, remove_keys=[], add_list_items=[]):
    """Get query params from request and return it as a list of tuples.
    e.g. [('content_types', '96')]"""
    query_params = request.query_params
    items = query_params.multi_items()
    items = [(key, value) for key, value in items if key not in remove_keys]
    items += add_list_items
    return items


async def get_str(request: Request, remove_keys=[], add_list_items=[]):
    """Get query params from request and return it as a quote plus encoded string.
    E.g. 'content_types=96&content_types=97&'"""

    items = await get_list(request, remove_keys=remove_keys)
    items += add_list_items
    query_str = await get_str_from_list(items)
    return query_str


async def get_str_from_list(items):
    """Get list of tuples and return it as a quote plus encoded string."""
    query_str = ""
    for key, value in items:
        query_str += f"{key}={quote_plus(value)}&"

    return query_str


async def get_search(request: Request):
    """Get search query "q" from request and return it as a string.
    E.g. 'test search'"""
    query_params = request.query_params
    q = query_params.get("q", "")
    return q
