from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core import flash
from stadsarkiv_client.core import api
from stadsarkiv_client.core.openaws import OpenAwsException
import json

log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_entity_create(request: Request):
    # Type needs to be altered to name
    # type is e.g. car
    # name is e.g. car_2 (the name of the schema '_' + version)

    try:
        schema = await api.schema_read(request)
        schema.type = schema.name
        schema = schema.to_dict()
        schema = json.dumps(schema)

        context_values = {"title": translate("Entities"), "schema": schema}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("entities/entities_create.html", context)

    except Exception as e:
        # for sure this is a 404
        raise HTTPException(404, detail=str(e), headers=None)


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def post_entity_create(request: Request):
    # {"data":{"make":"Toyota","year":2008,"model":"test","safety":-1},"schema":"car_1"}

    try:
        await api.entity_create(request)

    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return JSONResponse({"message": str(e)})
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_entities(request: Request):
    try:
        entities = await api.entities_read(request)
        context_values = {"title": translate("Entities"), "entities": entities}
        context = get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entities.html", context)

    except Exception as e:
        log.exception(e)


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_entity(request: Request):
    try:
        entity = await api.entity_read(request)
        entity = entity.to_dict()

        # schema is e.g. person_1
        schema_name: str = entity["schema"].split("_")[0]
        schema_version = entity["schema"].split("_")[1]

        schema = await api.schema_read_specific(request, schema_name, schema_version)
        schema = schema.to_dict()

        log.debug(schema)

        log.debug(entity)
        context_values = {"title": translate("Entities"), "entity": entity}
        context = get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entity.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)
