from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import dynamic_settings
import json
from stadsarkiv_client.core.logging import get_log

log = get_log()


async def test(request: Request):
    context = get_context(request)
    settings = dynamic_settings.settings
    settings_json = json.dumps(settings, indent=4)
    context["variables"] = settings_json
    return templates.TemplateResponse("test.html", context)
