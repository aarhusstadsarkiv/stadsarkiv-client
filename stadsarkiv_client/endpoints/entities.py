from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_schemas import APISchema
from stadsarkiv_client.api_client.api_entities import APIEntity
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash

log = get_log()


async def get_entity_create(request: Request):

    schema_type = request.path_params['schema_type']

    api_schema = APISchema(request=request)
    schema = await api_schema.get_schema(schema_type=schema_type, as_text=True)
    schema = schema.decode("utf-8")

    log.debug(schema)

    context_values = {"title": translate("Entities"), "schema": schema}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('entities/entities.html', context)


async def post_entity_create(request: Request):

    try:
        schema_type = request.path_params['schema_type']
        log.debug(schema_type)

        # get body json from request
        url = "/entities"
        json_body = await request.json()

        log.debug(schema_type)
        log.debug(json_body)

        api_schema = APIEntity(request=request)
        await api_schema.post_entity(url=url, data=json_body)

    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return JSONResponse({"message": "Hello, world!"})
