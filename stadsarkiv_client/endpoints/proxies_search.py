"""
Proxy for search records endpoints
"""

from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records.normalize_facets import NormalizeFacets
from stadsarkiv_client.core import query
from stadsarkiv_client.records import normalize_dates
from stadsarkiv_client.core.hooks import get_hooks


log = get_log()


def _get_search_pagination_data(request: Request, size: int, total: int):
    result = {}

    if total > 10000:
        total = 10000

    result["total"] = total

    start = int(request.query_params.get("start", 0))
    result["start"] = start

    size = int(request.query_params.get("size", size))
    result["size"] = size

    total_pages = (total // size) + (1 if total % size != 0 else 0)
    result["total_pages"] = total_pages

    current_page = (start // size) + 1
    result["current_page"] = current_page

    return result


def _get_dates(request: Request):
    """
    Get dates from request. Used in date search form
    """
    dates = {}
    dates_from = request.query_params.get("date_from", None)
    dates_to = request.query_params.get("date_to", None)

    # split dates. From format: yyyymmdd and not yyyy-mm-dd
    if dates_from:
        dates["from_year"], dates["from_month"], dates["from_day"] = dates_from[:4], dates_from[4:6], dates_from[6:]

    if dates_to:
        dates["to_year"], dates["to_month"], dates["to_day"] = dates_to[:4], dates_to[4:6], dates_to[6:]

    return dates


def _get_size_sort(request: Request):
    """
    Get size and sort from request. If not set in request, then get from cookies.
    If not set in cookie use some default values
    """
    size = request.query_params.get("size", request.cookies.get("size", "20"))
    sort = request.query_params.get("sort", request.cookies.get("sort", "date_from"))
    return size, sort


def _get_default_query_params(request: Request):
    """
    Get default query_params for records search as list of tuples:
    size, sort, direction
    """
    size, sort = _get_size_sort(request)
    add_list_items = [("size", size), ("sort", sort)]

    direction = None
    if sort == "date_to":
        direction = request.query_params.get("direction", "desc")

    if sort == "date_from":
        direction = request.query_params.get("direction", "asc")

    if direction:
        add_list_items.append(("direction", direction))

    # add start
    start = request.query_params.get("start", None)
    if start:
        add_list_items.append(("start", start))

    return add_list_items


def _normalize_search(records: dict):
    """
    Normalize date
    Get collection and content_type from facets_resolved
    These are displayed in the search result
    """
    facets_resolved = records["facets_resolved"]

    for record in records["result"]:
        record = normalize_dates.split_date_strings(record)
        record = normalize_dates.normalize_dates(record)

        # Add collection as string
        if "collection_id" in record and record["collection_id"]:
            record["collection"] = facets_resolved["collection"].get(record["collection_id"]).get("display_label", None)

        if "content_types" in record:
            content_type = record["content_types"][-1]
            record["content_type"] = facets_resolved["content_types"].get(content_type).get("display_label", None)

    return records


def _check_series(query_params: list) -> list:
    """
    Check if a collection is set in query params.
    If not then remove series from query params
    """
    collection = None
    for key, value in query_params:
        if key == "collection":
            collection = True

    for key, value in query_params:
        if key == "series" and not collection:
            query_params.remove((key, value))

    return query_params


async def get(request: Request):
    hooks = get_hooks(request)

    q = query.get_search(request)
    size, sort = _get_size_sort(request)
    add_list_items = _get_default_query_params(request)

    # size, sort, direction are read from query params
    # If not set they may be read from cookies
    # last resort is default values
    query_params_before_search = query.get_list(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    query_params_before_search = _check_series(query_params_before_search)

    # Alter query params before search
    # You may want to remove all collections and add single one before search results are obtained
    query_params_before_search = await hooks.before_get_search(query_params=query_params_before_search)

    # Call api
    query_str_search = query.get_str_from_list(query_params_before_search)
    search_result = await api.proxies_records(request, query_str_search)

    search_result = _normalize_search(search_result)

    # Alter query params after search
    # You may want to remove all collections.
    query_params_after_search = await hooks.after_get_search(query_params=query_params_before_search)

    # Remove pagination params from query params. In order to get a query string that can be used in e.g. facet links
    query_str_display = query.get_str_from_list(query_params_after_search, remove_keys=["start", "size", "sort", "direction"])

    normalized_facets = NormalizeFacets(
        request=request,
        records=search_result,
        query_params=query_params_after_search,
        query_str=query_str_display,
    )

    facets = normalized_facets.get_transformed_facets()
    facets_enabled = settings["facets_enabled"]

    # only use facets that are enabled in settings left menu
    facets = {key: value for key, value in facets.items() if key in facets_enabled}

    # sort by facets_enabled order
    facets = {key: facets[key] for key in facets_enabled}

    facets_filters = normalized_facets.get_filters()
    pagination_data = _get_search_pagination_data(request, search_result["size"], search_result["total"])

    context_values = {
        "q": q,
        "title": translate("Search"),
        "search_result": search_result,
        "query_params": query_params_after_search,
        "query_str_search": query_str_search,
        "query_str_display": query_str_display,
        "sort": sort,
        "size": size,
        "facets": facets,
        "facets_filters": facets_filters,
        "dates": _get_dates(request),
        "pagination_data": pagination_data,
    }

    DAYS_365 = 60 * 60 * 24 * 365 * 1

    context = await get_context(request, context_values=context_values)
    response = templates.TemplateResponse("search/search.html", context)

    search_cookie_value = {
        # Use site specific query params set before search
        "query_str_display": query_str_display,
        "query_params": query_params_before_search,
        "total": pagination_data["total"],
        "q": q,
    }

    response.set_cookie(key="search", value=json.dumps(search_cookie_value), httponly=True)
    response.set_cookie(key="size", value=size, httponly=True, max_age=DAYS_365, expires=DAYS_365)
    response.set_cookie(key="sort", value=sort, httponly=True, max_age=DAYS_365, expires=DAYS_365)

    return response


async def get_json(request: Request):
    add_list_items = _get_default_query_params(request)
    query_params = query.get_list(request, remove_keys=["size", "sort", "direction"], add_list_items=add_list_items)

    hooks = get_hooks(request)
    query_params = await hooks.before_get_search(query_params=query_params)
    query_str = query.get_str_from_list(query_params)
    search_result = await api.proxies_records(request, query_str)

    record_json = json.dumps(search_result, indent=4, ensure_ascii=False)
    return PlainTextResponse(record_json)


async def auto_complete(request: Request):
    """
    Auto complete for search
    """
    hooks = get_hooks(request)
    query_params: list = []
    query_params = await hooks.before_get_auto_complete(query_params=query_params)

    query_str = query.get_str_from_list(query_params)
    result = await api.proxies_auto_complete(request, query_str)

    query_params = await hooks.after_get_auto_complete(query_params=query_params)

    # randomly choose between 0 and 10 results
    # This is done to avoid showing all results
    # This is just for demo
    import random

    result = random.sample(result, random.randint(0, 10))

    return JSONResponse(result)
