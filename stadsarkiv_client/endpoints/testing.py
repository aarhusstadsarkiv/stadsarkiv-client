"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.core.context import get_context
from starlette.responses import HTMLResponse, PlainTextResponse
from stadsarkiv_client.core.templates import templates
import json

log = get_log()


async def test(request: Request):
    context_values = {"title": "TEST"}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse("testing/test.html", context)

    results = await api.proxies_entity_by_type("people", "121365")
    json_str = json.dumps(results, indent=4, ensure_ascii=False)
    return PlainTextResponse(json_str)
