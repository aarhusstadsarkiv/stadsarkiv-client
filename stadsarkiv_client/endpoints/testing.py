from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.dynamic_settings import settings
import json
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data import get_meta_data


log = get_log()


async def test(request: Request):
    settings_json = json.dumps(settings, indent=4, ensure_ascii=False)
    context_variables = {"settings": settings_json, "title": "Test"}
    context = await get_context(request, context_variables)
    return templates.TemplateResponse("testing/test.html", context)
