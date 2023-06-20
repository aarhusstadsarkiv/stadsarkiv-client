from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records.record_alter import record_alter, get_sections


log = get_log()


async def get_records_search(request: Request):
    query_params = {}
    q = ""
    if request.query_params:
        query_items = request.query_params.items()
        query_params = {k: v for k, v in query_items if k != "q"}
        q = request.query_params.get("q", "")

    records = await api.proxies_records(request)
    records_json = json.dumps(records, indent=4, ensure_ascii=False)
    context_values = {"title": translate("Search"), "records": records, "query_params": query_params, "q": q, "records_json": records_json}

    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("records/search.html", context)


async def get_record_view(request: Request):
    try:
        permissions = await api.me_permissions(request)
        record = await api.proxies_record_get(request)

        record_dict = record_alter(request, record)
        record_sections = get_sections(record_dict)

        if "administration" in record_sections and "employee" not in permissions:
            del record_sections["administration"]

        if "resources" in record_sections and "employee" not in permissions:
            del record_sections["resources"]

        context_values = {
            "me_permissions": permissions,
            "record": record_dict,
            "record_sections": record_sections,
        }

        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/record.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)


async def get_record_view_json(request: Request):
    try:
        record = await api.proxies_record_get(request)
        record_dict = record_alter(request, record)

        record_json = json.dumps(record_dict, indent=4, ensure_ascii=False)
        return PlainTextResponse(record_json)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)
