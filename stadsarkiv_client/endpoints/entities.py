from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils import api
from stadsarkiv_client.utils.openaws import OpenAwsException

log = get_log()


async def get_entity_create(request: Request):
    # Type needs to be altered to name
    # type is e.g. car
    # name is e.g. car_2 (the name of the schema '_' + version)
    try:
        schema = await api.get_schema(request)
        schema.type = schema.name
        schema = schema.to_dict()

        context_values = {"title": translate("Entities"), "schema": schema}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("entities/entities.html", context)

    except Exception as e:
        raise HTTPException(404, detail=str(e), headers=None)


async def post_entity_create(request: Request):
    # {"data":{"make":"Toyota","year":2008,"model":"test","safety":-1},"schema":"car_1"}
    try:
        await api.post_entity_create(request)

    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return JSONResponse({"message": str(e)})
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return JSONResponse({"message": "Hello, world!"})
