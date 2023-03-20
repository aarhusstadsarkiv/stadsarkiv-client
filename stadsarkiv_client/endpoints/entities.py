from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_schemas import APISchema
from stadsarkiv_client.api_client.api_base import APIException
from stadsarkiv_client.api_client.api_entities import APIEntity
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
import json

log = get_log()


async def get_entity_create(request: Request):
    schema_type = request.path_params["schema_type"]

    api_schema = APISchema(request=request)
    schema = await api_schema.get_schema(schema_type=schema_type)

    log.debug(schema)
    # Type needs to be altered to name
    # type is e.g. car
    # name is e.g. car_2 (the name of the schema '_' + version)
    schema["type"] = schema["name"]
    schema_json = json.dumps(schema)

    context_values = {"title": translate("Entities"), "schema": schema_json}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse("entities/entities.html", context)


async def post_entity_create(request: Request):
    try:
        # schema_type = request.path_params["schema_type"]

        # get body json from request
        url = "/entities"
        json_body = await request.json()

        log.debug(type(json_body))

        api_entity = APIEntity(request=request)
        await api_entity.post_entity(url=url, data=json_body)

    except APIException as e:
        log.exception(e)
        return JSONResponse({"message": str(e)})
        flash.set_message(request, str(e), type="error")

    return JSONResponse({"message": "Hello, world!"})
