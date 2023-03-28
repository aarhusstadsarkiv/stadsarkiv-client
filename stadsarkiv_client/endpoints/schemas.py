from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core import flash
from stadsarkiv_client.core import user
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.openaws import OpenAwsException
from stadsarkiv_client.core import api
from json import JSONDecodeError


log = get_log()


async def get_schemas(request: Request):
    await user.get_user(request)
    schemas = await api.schemas_read(request)
    context_values = {"title": translate("Schemas"), "schemas": schemas}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("schemas/schemas.html", context)


async def get_schema(request: Request):
    try:
        schema = await api.schema_read(request)
        schema = schema.to_dict()
        context_values = {"title": translate("Schemas"), "schema": schema}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("schemas/schema.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


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
