import json
from starlette.requests import Request


def get_search_cookie(request: Request) -> dict:
    """
    The search cookie contains the following data.
    It is set on every new search request

    "query_str_display" is a query string that can be used to display the last search query
    "query_params" is a list of tuples that can be used to make a new search query,
    "total": total number of results found
    "q" is the search query (e.g. "Some text search query")
    """

    try:
        search_cookie_str = request.cookies.get("search", None)
        assert isinstance(search_cookie_str, str)

        search_cookie = json.loads(search_cookie_str)
        assert isinstance(search_cookie, dict)

        # Query params is a list of tuples, but when converting to json it is converted to a list of lists
        # Convert back to list of tuples
        query_params = search_cookie["query_params"]
        query_params = [tuple(item) for item in query_params]
        search_cookie["query_params"] = query_params

        assert isinstance(search_cookie, dict)
        return search_cookie

    except Exception:
        return {}


def get_search_query_params(request: Request) -> list:
    """Get query string from search cookie and return it as a list of tuples.
    E.g. [('content_types', '96'), ('content_types', '97')]"""

    search_cookie = get_search_cookie(request)
    query_params = search_cookie.get("query_params", [])
    return query_params


def get_query_str_display(request: Request) -> str:
    """Get query string from search cookie and return it as a string.
    E.g. 'content_types=96&content_types=97&'"""

    search_cookie = get_search_cookie(request)
    query_str_display = search_cookie.get("query_str_display", "")
    return query_str_display
