from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils import user
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils.openaws import (
    # schema
    SchemaCreate,
    SchemaRead,
    SchemaCreateData,
    schemas_name_get,
    schemas_post,
    schemas_get,
    # client related
    AuthenticatedClient,
    get_auth_client,
    OpenAwsException,
)
from stadsarkiv_client.utils import api
from json import JSONDecodeError


log = get_log()


async def get_schemas(request: Request):
    await user.get_user(request)

    schemas = await api.get_schemas(request)

    context_values = {"title": translate("Schemas"), "schemas": schemas}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("schemas/schemas.html", context)


async def get_schema(request: Request):
    try:

        schema = api.get_schema(request)
        schema = schema.to_dict()
        context_values = {"title": translate("Schemas"), "schema": schema}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("schemas/schema.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


async def post_schema(request: Request):
    try:
        schema = await api.post_schema(request)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/schemas", status_code=302)
