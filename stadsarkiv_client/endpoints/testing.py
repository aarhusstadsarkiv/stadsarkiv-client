import typing
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.logging import log
from stadsarkiv_client.utils.fastapi_client import FastAPIClient
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils import dynamic_settings
import json


async def test(request: Request):

    context = get_context(request)
    settings = dynamic_settings.settings
    settings_json = json.dumps(settings, indent=4)
    context["variables"] = settings_json
    return templates.TemplateResponse('test.html', context)


    
