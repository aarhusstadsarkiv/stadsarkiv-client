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
from stadsarkiv_client.core.api import OpenAwsException
import json
from stadsarkiv_client.core.openaws import (
    SchemaRead,
    EntityRead,
)

log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["admin"])
async def get_entity_create(request: Request):
    try:
        schema: SchemaRead = await api.schema_read(request)
        schema_dict = schema.to_dict()

        """ Type needs to be altered to name before being used with the json editor
        type is e.g. car
        name is e.g. car_2 """

        schema_dict["type"] = schema_dict["name"]
        schema_json = json.dumps(schema_dict, indent=4, ensure_ascii=False)

        context_values = {"title": translate("Entities"), "schema": schema_json}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse("entities/entities_create.html", context)

    except Exception as e:
        # for sure this is a 404
        raise HTTPException(404, detail=str(e), headers=None)


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["admin"])
async def post_entity_create(request: Request):
    # {"data":{"make":"Toyota","year":2008,"model":"test","safety":-1},"schema":"car_1"}

    try:
        await api.entity_create(request)
        flash.set_message(request, translate("Entity created"), type="success", remove=True)
        return JSONResponse({"message": translate("Entity created"), "error": False})

    except OpenAwsException as e:
        log.exception(e)
        return JSONResponse({"message": translate("Entity could not be created"), "error": True})
    except Exception as e:
        log.exception(e)
        return JSONResponse({"message": translate("Entity could not be created"), "error": True})


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_entities(request: Request):
    try:
        entities: list[EntityRead] = await api.entities_read(request)
        context_values = {"title": translate("Entities"), "entities": entities}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entities.html", context)

    except Exception as e:
        log.exception(e)


def get_schema_and_values(schema, entity):
    schema_and_values = schema["data"]["properties"]
    data = entity["data"]

    for key, _value in schema_and_values.items():
        if key in data:
            schema_and_values[key]["value"] = data[key]

    return schema_and_values


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["admin"])
async def get_entity_view(request: Request):
    try:
        # content
        entity: EntityRead = await api.entity_read(request)
        entity_dict = entity.to_dict()

        # schema is e.g. person_1
        schema_name: str = entity_dict["schema_name"].split("_")[0]
        schema_version = entity_dict["schema_name"].split("_")[1]

        # schema
        schema = await api.schema_read_specific(request, schema_name, schema_version)
        schema_dict = schema.to_dict()

        schema_and_values = get_schema_and_values(schema_dict, entity_dict)

        context_values = {"title": translate("Entity"), "schema_and_values": schema_and_values}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entity.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)


__ALL__ = [
    "get_entity_create",
    "post_entity_create",
    "get_entities",
    "get_entity_view",
]
