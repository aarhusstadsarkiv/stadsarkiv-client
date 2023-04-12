from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api
from json import JSONDecodeError
import json


log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_schemas(request: Request):
    try:
        schemas = await api.schemas_read(request)
        context_values = {"title": translate("Schemas"), "schemas": schemas}
        context = get_context(request, context_values=context_values)
        return templates.TemplateResponse("schemas/schemas.html", context)
    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_schema(request: Request):
    try:
        schema = await api.schema_read(request)
        schema = schema.to_dict()
        schema_json = json.dumps(schema, indent=4, ensure_ascii=False)
        context_values = {"title": translate("Schemas"), "schema": schema_json}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("schemas/schema.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def post_schema(request: Request):
    try:
        await api.schema_create(request)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/schemas", status_code=302)
