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
from stadsarkiv_client.core import cookie
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
import asyncio
import json


log = get_log()


def _get_altered_cookie(request: Request):
    try:
        search_cookie = cookie.get_search_cookie(request)

        # change query size to 1 in order to just get single record
        query_params = search_cookie["query_params"]
        query_params = [tuple(item) for item in query_params if item[0] != "size"]
        query_params.append(("size", "1"))
        search_cookie["query_params"] = query_params
        return search_cookie

    except Exception:
        return None


async def _get_record_pagination(request: Request):
    # 'search' as a 'get' param indicates that we came from a search.
    # It is used as the current page number in the pagination
    # If not present then the prev and next buttons should not be shown
    current_page = int(request.query_params.get("search", 0))
    if not current_page:
        return None

    search_cookie = _get_altered_cookie(request)
    if not search_cookie:
        return None

    query_params = search_cookie["query_params"]

    has_next = current_page < search_cookie["total"]
    has_prev = current_page > 1

    next_page = current_page + 1 if has_next else None
    prev_page = current_page - 1 if has_prev else None

    record_pagination = {}

    # last query string is used to generate a link to last search result
    record_pagination["query_str_display"] = search_cookie["query_str_display"]
    record_pagination["total"] = search_cookie["total"]
    record_pagination["next_page"] = next_page
    record_pagination["prev_page"] = prev_page

    async def get_next_record():
        if next_page:
            next_query_params = query_params.copy()
            search_params = [("start", str(next_page - 1))]
            next_query_params.extend(search_params)
            records = await api.proxies_records_from_list(request, next_query_params)
            return records["result"][0]["id"]
        else:
            return None

    async def get_prev_record():
        if prev_page:
            prev_query_params = query_params.copy()
            search_params = [("start", str(prev_page - 1))]
            prev_query_params.extend(search_params)
            records = await api.proxies_records_from_list(request, prev_query_params)
            return records["result"][0]["id"]
        else:
            return None

    # Gather both API calls concurrently
    next_record, prev_record = await asyncio.gather(get_next_record(), get_prev_record())

    record_pagination["next_record"] = next_record
    record_pagination["prev_record"] = prev_record
    record_pagination["current_page"] = current_page

    return record_pagination


async def get(request: Request):
    hooks = get_hooks(request)

    record_id = request.path_params["record_id"]

    record_pagination, permissions, record = await asyncio.gather(
        _get_record_pagination(request), api.me_permissions(request), api.proxies_record_get_by_id(request, record_id)
    )

    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    record_altered = record_alter.record_alter(request, record, meta_data)
    record_and_types = record_alter.get_record_and_types(record_altered)

    context_variables = {
        "is_employee": "employee" in permissions,
        "title": meta_data["title"],
        "meta_title": meta_data["meta_title"],
        "meta_description": meta_data["meta_description"],
        "meta_data": meta_data,
        "record_and_types": record_and_types,
        "record_pagination": record_pagination,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse(request, "records/record.html", context)


async def get_json(request: Request):
    try:
        hooks = get_hooks(request)

        record_id = request.path_params["record_id"]
        type = request.path_params["type"]

        record = await api.proxies_record_get_by_id(request, record_id)
        meta_data = get_record_meta_data(request, record)
        record, meta_data = await hooks.after_get_record(record, meta_data)

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
