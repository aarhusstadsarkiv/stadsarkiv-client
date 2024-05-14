"""
Endpoints for schemas.
"""

from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, JSONResponse
from stadsarkiv_client.core.auth import is_authenticated
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api
from json import JSONDecodeError


log = get_log()


async def get_list(request: Request):
    await is_authenticated(request, permissions=["admin"])
    try:
        schemas = await api.schemas(request)
        context_values = {"title": translate("Schemas"), "schemas": schemas}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse(request, "schemas/schemas.html", context)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


async def get_single(request: Request):
    try:
        schema = await api.schema_get(request)
        return JSONResponse(schema)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


async def post(request: Request):
    await is_authenticated(request, permissions=["admin"])
    try:
        await api.schema_create(request)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/schemas", status_code=302)
