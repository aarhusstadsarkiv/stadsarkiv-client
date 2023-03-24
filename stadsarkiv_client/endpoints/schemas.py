from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_schemas import APISchema
from stadsarkiv_client.api_client.api_base import APIBase
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils import user
from stadsarkiv_client.api_client.api_base import APIException
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
    Client,
    get_client,
    get_auth_client,
    HTTPValidationError,
    OpenAwsException,
)
from json import JSONDecodeError
import json

log = get_log()


async def get_schemas(request: Request):
    await user.get_user(request)

    client: Client = get_auth_client(request)
    schemas = schemas_get.sync(client=client, limit=1000)

    context_values = {"title": translate("Schemas"), "schemas": schemas}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("schemas/schemas.html", context)


async def get_schema(request: Request):

    try:
        await user.get_user(request)

        schema_type = request.path_params["schema_type"]
        client: Client = get_auth_client(request)

        schema = schemas_name_get.sync(client=client, name=schema_type, version=None)
        if not isinstance(schema, SchemaRead):
            log.exception(schema)
            raise OpenAwsException(
                translate("Schema not found."),
                422,
                "Unauthorized",
            )
        if (isinstance(schema, SchemaRead)):
            schema = schema.to_dict()
            log.debug(schema)

            context_values = {"title": translate("Schemas"), "schema": schema}
            context = get_context(request, context_values=context_values)

            return templates.TemplateResponse("schemas/schema.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


async def post_schema(request: Request):
    try:
        form = await request.form()
        schema_type = str(form.get("type"))
        data = str(form.get("data"))

        data_dict = {}
        data_dict["type"] = schema_type

        src_dict = json.loads(data)

        client: Client = get_auth_client(request)
        schema = schemas_post.sync(client=client, json_body=SchemaCreate(
            type=schema_type, data=SchemaCreateData.from_dict(src_dict=src_dict)))

        if (isinstance(schema, SchemaRead)):
            log.debug(schema)
        else:
            raise OpenAwsException(translate('Schema could not be created'), 500)

        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/schemas", status_code=302)
