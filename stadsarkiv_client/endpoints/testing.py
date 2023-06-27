from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.dynamic_settings import settings
import json
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.records.record_alter import record_alter


log = get_log()


async def test(request: Request):
    settings_json = json.dumps(settings, indent=4, ensure_ascii=False)
    context_variables = {"settings": settings_json, "title": "Test"}
    context = await get_context(request, context_variables)
    return templates.TemplateResponse("testing/test.html", context)


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


async def test_entitites_macro(request: Request):
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
