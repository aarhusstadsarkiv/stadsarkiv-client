from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from starlette.responses import PlainTextResponse
import json

log = get_log()


async def test(request: Request):
    # settings_json = json.dumps(settings, indent=4, ensure_ascii=False)
    # context_variables = {"settings": settings_json, "title": "Test"}
    # context = await get_context(request, context_variables)
    # return templates.TemplateResponse("testing/test.html", context)
    # results = await api.proxies_records_from_list([("size", "10"), ("q", "hvilsager"), ("view", "ids")])

    results = await api.proxies_entity_by_type("people", "121365")
    json_str = json.dumps(results, indent=4, ensure_ascii=False)
    return PlainTextResponse(json_str)
