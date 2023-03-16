from starlette.requests import Request
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
from json import JSONDecodeError
import json

log = get_log()


async def get_schemas(request: Request):
    await user.get_user(request)

    api_schema = APISchema(request=request)
    schemas = await api_schema.get_schemas()

    context_values = {"title": translate("Schemas"), "schemas": schemas}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("schemas/schemas.html", context)


async def get_schema(request: Request):
    await user.get_user(request)

    schema_type = request.path_params["schema_type"]

    api_schema = APISchema(request=request)
    schema = await api_schema.get_schema(schema_type=schema_type)

    context_values = {"title": translate("Schemas"), "schema": schema}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("schemas/schema.html", context)


async def post_schema(request: Request):
    try:
        form = await request.form()
        type = str(form.get("type"))
        data = str(form.get("data"))

        data_dict = {}
        data_dict["type"] = type

        data = json.loads(data)
        data_dict["data"] = data

        schema = APIBase(request=request)
        schema.jwt_post_json(url="/schemas/", data=data_dict)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/schemas", status_code=302)
