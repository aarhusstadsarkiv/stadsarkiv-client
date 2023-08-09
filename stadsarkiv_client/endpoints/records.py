from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.normalize_facets import NormalizeFacets
from stadsarkiv_client.records.meta_data import get_meta_data
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import query
from stadsarkiv_client.records.normalize_abstract_dates import normalize_abstract_dates


log = get_log()


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


async def _get_record_pagination_data(request: Request):
    search_query = request.query_params.get("search", None)
    if not search_query:
        return None

    """Use search cooke and request param 'search' to calculate pagination data for record view"""
    search_cookie = request.cookies.get("search", None)

    if not search_cookie:
        return None

    try:
        search_cookie = json.loads(search_cookie)
        assert isinstance(search_cookie, dict)

        query_params = search_cookie["query_params"]

        # Use for record pagination. Size must be 1.
        # Other query params can be used
        query_params = [item for item in query_params if item[0] != "size"]
        query_params.append(("size", "1"))

        # convert list of lists to list of tuples
        query_params = [tuple(item) for item in query_params]
        search_cookie["query_params"] = query_params

    except Exception:
        return None

    return search_cookie


async def _get_record_prev_next(request: Request, search_query_params):
    current_page = int(request.query_params.get("search", 0))

    has_next = current_page < search_query_params["total"]
    has_prev = current_page > 1

    next_page = current_page + 1 if has_next else None
    prev_page = current_page - 1 if has_prev else None

    search_query_params["next_page"] = next_page
    search_query_params["prev_page"] = prev_page

    query_params = search_query_params["query_params"]

    if next_page:
        start = ("start", str(next_page - 1))
        query_params.append(start)
        records = await api.proxies_records_from_list(query_params)
        search_query_params["next_record"] = records["result"][0]["id"]
    else:
        search_query_params["next_record"] = None

    if prev_page:
        start = ("start", str(prev_page - 1))
        query_params.append(start)
        records = await api.proxies_records_from_list(query_params)
        search_query_params["prev_record"] = records["result"][0]["id"]
    else:
        search_query_params["prev_record"] = None

    return search_query_params


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
    """Get default query_params for records search."""

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
    for record in records["result"]:
        record = normalize_abstract_dates(record, split=True)
    return records


async def get_records_search(request: Request):
    q = await query.get_search(request)
    size, sort = _get_size_sort(request)
    add_list_items = _get_default_query_params(request)

    # size, sort, direction are read from query params
    # If not set they may be read from cookies
    # last resort is default values
    query_params = await query.get_list(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    query_str = await query.get_str(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    records = await api.proxies_records(request, remove_keys=["size", "sort", "direction"], add_list_items=add_list_items)
    records = _normalize_search(records)

    normalized_facets = NormalizeFacets(request=request, records=records, query_params=query_params, query_str=query_str)
    facets = normalized_facets.get_transformed_facets()
    facets_filters = normalized_facets.get_checked_facets()
    pagination_data = _get_search_pagination_data(request, records["size"], records["total"])

    context_values = {
        "q": q,
        "title": translate("Search"),
        "records": records,
        "query_params": query_params,
        "query_str": query_str,
        "sort": sort,
        "size": size,
        "record_facets": records["facets"],
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
        "q": q
        # "total_pages": pagination_data["total_pages"],
    }

    response.set_cookie(key="search", value=json.dumps(search_cookie_value), httponly=True)
    response.set_cookie(key="size", value=size, httponly=True, max_age=DAYS_365, expires=DAYS_365)
    response.set_cookie(key="sort", value=sort, httponly=True, max_age=DAYS_365, expires=DAYS_365)

    return response


async def get_records_search_json(request: Request):
    add_list_items = _get_default_query_params(request)
    records = await api.proxies_records(request, add_list_items=add_list_items)
    records = _normalize_search(records)
    record_json = json.dumps(records, indent=4, ensure_ascii=False)
    return PlainTextResponse(record_json)


async def get_record_view(request: Request):
    record_pagination = await _get_record_pagination_data(request)
    if record_pagination:
        record_pagination = await _get_record_prev_next(request, record_pagination)

    record_id = request.path_params["record_id"]
    record_sections = settings["record_sections"]
    record_sections_employee = settings["record_sections_employee"]
    permissions = await api.me_permissions(request)
    record = await api.proxies_record_get_by_id(record_id)

    metadata = get_meta_data(request, record)
    record = {**record, **metadata}

    record_altered = record_alter.record_alter(request, record)
    record_and_types = record_alter.get_record_and_types(record_altered)
    sections = record_alter.get_section_data(record_sections, record_and_types)

    if "employee" not in permissions:
        for section in record_sections_employee:
            if section in sections:
                del sections[section]

    context_variables = {
        "title": record_altered["title"],
        "meta_title": record_altered["meta_title"],
        "record_altered": record_altered,
        "sections": sections,
        "record_pagination": record_pagination,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/record.html", context)


async def get_record_view_json(request: Request):
    try:
        record_id = request.path_params["record_id"]
        type = request.path_params["type"]
        record_sections = settings["record_sections"]

        record = await api.proxies_record_get_by_id(record_id)

        metadata = get_meta_data(request, record)
        record_altered = {**record, **metadata}

        record_altered = record_alter.record_alter(request, record_altered)
        record_and_types = record_alter.get_record_and_types(record_altered)
        sections = record_alter.get_section_data(record_sections, record_and_types)

        if type == "record":
            record_json = json.dumps(record, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_json)

        elif type == "record_altered":
            record_altered_json = json.dumps(record_altered, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_altered_json)

        elif type == "record_and_types":
            record_and_types_json = json.dumps(record_and_types, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_and_types_json)

        elif type == "record_sections":
            record_sections_json = json.dumps(sections, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_sections_json)
        else:
            raise HTTPException(404, detail="type not found", headers=None)

    except Exception as e:
        log.exception(e)
        raise HTTPException(500, detail=str(e), headers=None)
