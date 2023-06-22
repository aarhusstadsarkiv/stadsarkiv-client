from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import dynamic_settings
import json
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api


log = get_log()


async def test(request: Request):
    settings = dynamic_settings.settings
    settings_json = json.dumps(settings, indent=4, ensure_ascii=False)
    context_variables = {"settings": settings_json, "title": "Test"}
    context = await get_context(request, context_variables)
    return templates.TemplateResponse("testing/test.html", context)


def extract_data(sections, data):
    extracted_data = {}

    for section, keys in sections.items():
        extracted_values = {}
        for key in keys:
            if key in data:
                extracted_values[key] = data[key]

        if extracted_values:
            extracted_data[section] = extracted_values

    return extracted_data


async def test_entitites_macro(request: Request):
    record_id = request.path_params["record_id"]
    settings = dynamic_settings.settings
    record_sections = settings["record_sections"]

    entity = await api.proxies_record_get_by_id(record_id)
    sections = extract_data(record_sections, entity)

    entity_json = json.dumps(entity, indent=4, ensure_ascii=False)
    context_variables = {"title": "Test entities macro", "entity": entity, "entity_json": entity_json, "sections": sections}

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("testing/test_entities_macro.html", context)
