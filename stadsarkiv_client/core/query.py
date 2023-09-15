"""
Some query utils that can be used to get query params from request and return it as a list of tuples or a string.
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from urllib.parse import quote_plus

log = get_log()


def get_list(request: Request, remove_keys: list = [], add_list_items: list = []) -> list:
    """Get query params from request and return it as a list of tuples.
    e.g. [('content_types', '96')]"""
    query_params = request.query_params
    items = query_params.multi_items()
    items = [(key, value) for key, value in items if key not in remove_keys]
    items += add_list_items
    return items


def get_str(request: Request, remove_keys: list = [], add_list_items: list = []) -> str:
    """Get query params from request and return it as a quote plus encoded string.
    E.g. 'content_types=96&content_types=97&'"""

    items = get_list(request, remove_keys=remove_keys)
    items += add_list_items
    query_str = get_str_from_list(items)
    return query_str


def get_str_from_list(items: list) -> str:
    """Get list of tuples and return it as a quote plus encoded string."""
    query_str = ""
    for key, value in items:
        query_str += f"{key}={quote_plus(value)}&"

    return query_str


def get_search(request: Request) -> str:
    """Get search query "q" from request and return it as a string.
    E.g. 'test search'"""
    query_params = request.query_params
    q = query_params.get("q", "")
    return q
