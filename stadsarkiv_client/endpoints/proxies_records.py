"""
Proxy for records endpoints
"""

from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.core import api
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
import asyncio
import json


hooks = get_hooks()
log = get_log()


async def _get_last_search_cookie(request: Request):
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


async def _get_record_prev_next(request: Request):
    search_query_params = await _get_last_search_cookie(request)
    if not search_query_params:
        return None

    current_page = int(request.query_params.get("search", 0))
    if not current_page:
        return None

    has_next = current_page < search_query_params["total"]
    has_prev = current_page > 1

    next_page = current_page + 1 if has_next else None
    prev_page = current_page - 1 if has_prev else None

    search_query_params["next_page"] = next_page
    search_query_params["prev_page"] = prev_page

    query_params = search_query_params["query_params"].copy()

    async def get_next_record():
        if next_page:
            next_query_params = query_params.copy()
            search_params = [("start", str(next_page - 1))]
            next_query_params.extend(search_params)
            records = await api.proxies_records_from_list(next_query_params)
            return records["result"][0]["id"]
        else:
            return None

    async def get_prev_record():
        if prev_page:
            prev_query_params = query_params.copy()
            search_params = [("start", str(prev_page - 1))]
            prev_query_params.extend(search_params)
            records = await api.proxies_records_from_list(prev_query_params)
            return records["result"][0]["id"]
        else:
            return None

    # Gather both API calls concurrently
    next_record, prev_record = await asyncio.gather(get_next_record(), get_prev_record())

    search_query_params["next_record"] = next_record
    search_query_params["prev_record"] = prev_record
    search_query_params["current_page"] = current_page
    search_query_params["query_str_display"] = search_query_params["query_str_display"]

    return search_query_params


async def get_record_view(request: Request):
    record_pagination = await _get_record_prev_next(request)
    record_id = request.path_params["record_id"]
    permissions = await api.me_permissions(request)

    record = await api.proxies_record_get_by_id(record_id)
    record = hooks.after_record(record)

    meta_data = get_record_meta_data(request, record)

    record_altered = record_alter.record_alter(request, record, meta_data)
    record_and_types = record_alter.get_record_and_types(record_altered)

    context_variables = {
        "is_employee": "employee" in permissions,
        "title": meta_data["title"],
        "meta_title": meta_data["meta_title"],
        "meta_data": meta_data,
        "record_and_types": record_and_types,
        "record_pagination": record_pagination,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/record.html", context)


async def get_record_view_json(request: Request):
    try:
        record_id = request.path_params["record_id"]
        type = request.path_params["type"]

        record = await api.proxies_record_get_by_id(record_id)
        record = hooks.after_record(record)

        meta_data = get_record_meta_data(request, record)

        record_altered = record_alter.record_alter(request, record, meta_data)
        record_and_types = record_alter.get_record_and_types(record_altered)

        if type == "record":
            record_json = json.dumps(record, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_json)

        elif type == "meta_data":
            meta_data_json = json.dumps(meta_data, indent=4, ensure_ascii=False)
            return PlainTextResponse(meta_data_json)

        elif type == "record_and_types":
            record_and_types_json = json.dumps(record_and_types, indent=4, ensure_ascii=False)
            return PlainTextResponse(record_and_types_json)
        else:
            raise HTTPException(404, detail="type not found", headers=None)

    except Exception as e:
        log.exception(e)
        raise HTTPException(500, detail=str(e), headers=None)
