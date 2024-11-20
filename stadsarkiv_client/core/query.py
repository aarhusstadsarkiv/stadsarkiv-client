"""
Some query utils that can be used to get query params from request and return it as a list of tuples or a string.
"""

from starlette.requests import Request
from urllib.parse import quote_plus
from stadsarkiv_client.core.logging import get_log

log = get_log()


def get_list(request: Request, accept_keys: list = [], default_query_params: list = []) -> list:
    """
    Get query params from request and return it as a list of tuples.
    e.g. [('content_types', '96')]
    """
    query_params = request.query_params
    items = query_params.multi_items()

    items = [(key, value) for key, value in items if key in accept_keys]
    items.extend(default_query_params)

    return items


def get_str_from_list(query_params: list, accept_keys: list = [], remove_keys: list = []) -> str:
    """Get list of tuples and return it as a quote plus encoded string."""

    # hack to remove leading zeros
    # trim all "0" from items value. Eg. "000096" -> "96" except if value is "0"
    query_params_used = [(key, value.lstrip("0")) if value != "0" else (key, value) for key, value in query_params]

    query_str = ""

    if accept_keys:
        query_params_used = [(key, value) for key, value in query_params_used if key in accept_keys]
    else:
        query_params_used = [(key, value) for key, value in query_params_used]

    if remove_keys:
        query_params_used = [(key, value) for key, value in query_params_used if key not in remove_keys]

    for key, value in query_params_used:
        value = quote_plus(value)
        query_str += f"{key}={value}&"

    return query_str


def get_search(request: Request) -> str:
    """Get search query "q" from request and return it as a string.
    E.g. 'test search'"""
    query_params = request.query_params
    q = query_params.get("q", "")
    return q
