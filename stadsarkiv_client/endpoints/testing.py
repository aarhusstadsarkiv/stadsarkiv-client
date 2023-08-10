from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from starlette.responses import JSONResponse

log = get_log()


async def test(request: Request):
    # settings_json = json.dumps(settings, indent=4, ensure_ascii=False)
    # context_variables = {"settings": settings_json, "title": "Test"}
    # context = await get_context(request, context_variables)
    # return templates.TemplateResponse("testing/test.html", context)
    results = await api.proxies_records_from_list([("size", "10"), ("q", "hvilsager"), ("view", "ids")])
    return JSONResponse(results)
