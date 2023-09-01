from starlette.requests import Request
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records.normalize_facets import NormalizeFacets
from stadsarkiv_client.core import query
from stadsarkiv_client.records.normalize_abstract_dates import normalize_abstract_dates
from stadsarkiv_client.facets import QUERY_PARAMS


log = get_log()


def _get_resource_types():
    resource_types = []

    # Get all resource types
    for key, value in QUERY_PARAMS.items():
        if value.get("entity", False):
            resource_types.append(key)

    return resource_types


def _get_search_pagination_data(request: Request, size, total):
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
    """Get size and sort from request. If not request, get from cookies. Or default"""
    size = request.query_params.get("size", request.cookies.get("size", "20"))
    sort = request.query_params.get("sort", request.cookies.get("sort", "date_from"))
    return size, sort


def _get_default_query_params(request: Request):
    """Get default query_params for records search as list of tuples"""

    size, sort = _get_size_sort(request)
    add_list_items = [("size", size), ("sort", sort)]

    direction = None
    if sort == "date_to":
        direction = request.query_params.get("direction", "desc")

    if sort == "date_from":
        direction = request.query_params.get("direction", "asc")

    if direction:
        add_list_items.append(("direction", direction))

    return add_list_items


def _normalize_search(records):
    """Normalize search records"""
    facets_resolved = records["facets_resolved"]

    for record in records["result"]:
        record = normalize_abstract_dates(record, split=True)

        # Add collection as string
        if "collection_id" in record and record["collection_id"]:
            record["collection"] = facets_resolved["collection"].get(record["collection_id"]).get("display_label", None)

        if "content_types" in record:
            content_type = record["content_types"][-1]
            record["content_type"] = facets_resolved["content_types"].get(content_type).get("display_label", None)

    return records


def _get_resolve_query_str(query_params: list, record_params: list):
    resource_types = _get_resource_types()
    resolve_query_params = [(k, v) for k, v in query_params if k in resource_types]

    resolve_query_params.extend(record_params)
    resolve_query_params = list(set(resolve_query_params))

    resolve_query_string = query.get_str_from_list(resolve_query_params)
    return resolve_query_string


def _get_resolve_records(records: list):
    """resolve collection and content_types from records"""
    resolve_records = []
    for record in records:
        if "collection_id" in record and record["collection_id"]:
            resolve_records.append(("collection", record["collection_id"]))
        if "content_types" in record:
            type = record["content_types"][-1]
            resolve_records.append(("content_types", type))
    return resolve_records


async def get_records_search(request: Request):
    q = query.get_search(request)
    size, sort = _get_size_sort(request)
    add_list_items = _get_default_query_params(request)

    # size, sort, direction are read from query params
    # If not set they may be read from cookies
    # last resort is default values
    query_params = query.get_list(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    query_str = query.get_str(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    search_result = await api.proxies_records(request, remove_keys=["size", "sort", "direction"], add_list_items=add_list_items)

    # resolve facets
    result_params = _get_resolve_records(search_result["result"])
    resolve_query_str = _get_resolve_query_str(query_params, result_params)
    facets_resolved = await api.proxies_resolve(query_str=resolve_query_str)
    search_result["facets_resolved"] = facets_resolved
    search_result = _normalize_search(search_result)

    normalized_facets = NormalizeFacets(
        request=request, records=search_result, query_params=query_params, facets_resolved=facets_resolved, query_str=query_str
    )

    facets = normalized_facets.get_transformed_facets()
    facets_filters = normalized_facets.get_checked_facets()
    pagination_data = _get_search_pagination_data(request, search_result["size"], search_result["total"])

    context_values = {
        "q": q,
        "title": translate("Search"),
        "search_result": search_result,
        "query_params": query_params,
        "query_str": query_str,
        "sort": sort,
        "size": size,
        "facets": facets,
        "facets_filters": facets_filters,
        "dates": _get_dates(request),
        "pagination_data": pagination_data,
    }

    DAYS_365 = 60 * 60 * 24 * 365 * 1

    context = await get_context(request, context_values=context_values)
    response = templates.TemplateResponse("records/search.html", context)

    search_cookie_value = {
        "query_params": query_params,
        "total": pagination_data["total"],
        "q": q,
        "query_str": query_str,
    }

    response.set_cookie(key="search", value=json.dumps(search_cookie_value), httponly=True)
    response.set_cookie(key="size", value=size, httponly=True, max_age=DAYS_365, expires=DAYS_365)
    response.set_cookie(key="sort", value=sort, httponly=True, max_age=DAYS_365, expires=DAYS_365)

    return response


async def get_records_search_json(request: Request):
    add_list_items = _get_default_query_params(request)
    records = await api.proxies_records(request, add_list_items=add_list_items)
    record_json = json.dumps(records, indent=4, ensure_ascii=False)
    return PlainTextResponse(record_json)
