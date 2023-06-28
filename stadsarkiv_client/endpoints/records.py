from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.records.record_alter import record_alter
from stadsarkiv_client.core.dynamic_settings import settings


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


def get_section_data(sections, data):
    section_data = {}

    for section, keys in sections.items():
        section_values = {}
        for key in keys:
            if key in data:
                section_values[key] = data[key]

        if section_values:
            section_data[section] = section_values

    return section_data


def get_record_and_types(record):
    record_altered = {}
    for key, value in record.items():
        record_item = {}
        record_item["value"] = value
        record_item["name"] = key

        try:
            definition = settings["record_definitions"][key]
            record_item["type"] = definition["type"]
        except KeyError:
            record_item["type"] = "unknown"

        record_altered[key] = record_item

    return record_altered


async def get_record_view(request: Request):
    record_id = request.path_params["record_id"]

    record = await api.proxies_record_get_by_id(record_id)
    record_altered = record_alter(request, record)

    record_sections = settings["record_sections"]
    record_and_types = get_record_and_types(record_altered)

    sections = get_section_data(record_sections, record_and_types)
    context_variables = {
        "title": record_altered["title"],
        "record_original": record,
        "record_and_types": record_and_types,
        "record_altered": record_altered,
        "sections": sections,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/record.html", context)


async def get_record_view_json(request: Request):
    try:
        record_id = request.path_params["record_id"]
        record = await api.proxies_record_get_by_id(record_id)
        record_altered = record_alter(request, record)

        record_sections = settings["record_sections"]
        record_and_types = get_record_and_types(record_altered)

        sections = get_section_data(record_sections, record_and_types)

        record_json = json.dumps(record, indent=4, ensure_ascii=False)
        return PlainTextResponse(record_json)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)
