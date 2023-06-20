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


async def test_entitites_macro(request: Request):
    context_variables = {"title": "Test entities macro"}

    record_id = "000110308"

    record = await api.proxies_record_get_by_id(record_id)
    log.debug(record)

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("testing/test_entities_macro.html", context)
