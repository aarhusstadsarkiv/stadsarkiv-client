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


log = get_log()


def _get_pagination_data(request: Request, size, total):
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
    """Get default query_params for records search"""

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


async def get_records_search(request: Request):
    size, sort = _get_size_sort(request)
    add_list_items = _get_default_query_params(request)
    query_params = await query.get_list(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)
    query_str = await query.get_str(request, remove_keys=["start", "size", "sort", "direction"], add_list_items=add_list_items)

    records = await api.proxies_records(request, add_list_items=add_list_items)
    normalized_facets = NormalizeFacets(request=request, records=records, query_params=query_params, query_str=query_str)
    facets = normalized_facets.get_transformed_facets()
    facets_filters = normalized_facets.get_checked_facets()
    pagination_data = _get_pagination_data(request, records["size"], records["total"])

    context_values = {
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
    response.set_cookie(key="size", value=size, httponly=True, max_age=DAYS_365, expires=DAYS_365)
    response.set_cookie(key="sort", value=sort, httponly=True, max_age=DAYS_365, expires=DAYS_365)

    return response


async def get_records_search_json(request: Request):
    add_list_items = _get_default_query_params(request)
    records = await api.proxies_records(request, add_list_items=add_list_items)
    record_json = json.dumps(records, indent=4, ensure_ascii=False)
    return PlainTextResponse(record_json)


async def get_record_view(request: Request):
    record_id = request.path_params["record_id"]
    record_sections = settings["record_sections"]

    record = await api.proxies_record_get_by_id(record_id)

    metadata = get_meta_data(request, record)
    record = {**record, **metadata}

    record_altered = record_alter.record_alter(request, record)
    record_and_types = record_alter.get_record_and_types(record_altered)
    sections = record_alter.get_section_data(record_sections, record_and_types)

    context_variables = {
        "title": record_altered["title"],
        "record_altered": record_altered,
        "sections": sections,
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
