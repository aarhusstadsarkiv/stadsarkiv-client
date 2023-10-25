""""
Entities endpoints
"""

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
import asyncio
import json


log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["employee"])
async def get_entity_create(request: Request):
    try:
        schema = await api.schema_get(request)

        """ Type needs to be altered to name before being used with the json editor
        type is e.g. car
        name is e.g. car_2 """

        schema["type"] = schema["name"]
        schema_json = json.dumps(schema, indent=4, ensure_ascii=False)

        context_values = {"title": "Opret entitet", "schema_json": schema_json}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse("entities/entities_create.html", context)

    except Exception as e:
        raise HTTPException(403, detail=str(e), headers=None)


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["employee"])
async def get_entity_update(request: Request):
    try:
        entity = await api.entity_get(request)

        schema_name = entity["schema_name"]
        schema_version = schema_name.split("_")[1]
        schema_name = schema_name.split("_")[0]

        schema = await api.schema_get_version(request, schema_name, schema_version)

        """ Type needs to be altered to name before being used with the json editor
        type is e.g. car
        name is e.g. car_2 """

        schema["type"] = schema["name"]
        schema_json = json.dumps(schema, indent=4, ensure_ascii=False)

        entity_data = entity["data"]
        entity_json = json.dumps(entity_data, indent=4, ensure_ascii=False)

        context_values = {"title": "Opdater entitet", "schema_json": schema_json, "entity_json": entity_json, "entity": entity}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse("entities/entities_update.html", context)

    except Exception as e:
        raise HTTPException(404, detail=str(e), headers=None)


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["employee"])
async def post_entity_create(request: Request):
    try:
        await api.entity_post(request)
        flash.set_message(request, "Entitet oprettet", type="success", remove=True)
        return JSONResponse({"message": translate("Entitet oprettet"), "error": False})

    except Exception:
        log.info("Entity create error", exc_info=True)
        return JSONResponse({"message": "Entitet kunne ikke oprettes", "error": True})


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["employee"])
async def patch_entity(request: Request):
    try:
        await api.entity_patch(request)
        flash.set_message(request, "Entitet opdateret", type="success", remove=True)
        return JSONResponse({"message": "Entitet opdateret", "error": False})

    except Exception:
        log.info("Entity update error", exc_info=True)
        return JSONResponse({"message": "Entitet kunne ikke opdateres", "error": True})


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["employee"])
async def entities_delete_soft(request: Request):
    if request.method == "POST":
        try:
            await api.entity_delete_soft(request)
            return JSONResponse({"message": "Entitet er slettet (soft)", "error": False})

        except Exception:
            log.info("Entity delete error", exc_info=True)
            return JSONResponse({"message": "Entitet kunne ikke slettes. Måske den allerede er slettet.", "error": True})

    try:
        uuid = request.path_params["uuid"]
        context_values = {"title": "Slet entitet", "uuid": uuid}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entities_delete_soft.html", context)

    except Exception as e:
        raise HTTPException(404, detail=str(e), headers=None)


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def get_entities(request: Request):
    try:
        entities, schemas = await asyncio.gather(api.entities_get(request), api.schemas(request))

        context_values = {"title": "Opret entiteter", "schemas": schemas, "entities": entities}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entities.html", context)

    except Exception as e:
        raise HTTPException(404, detail=str(e), headers=None)


def _get_schema_and_values(schema, entity):
    schema_and_values = schema["data"]["properties"]
    data = entity["data"]

    for key, _value in schema_and_values.items():
        if key in data:
            schema_and_values[key]["value"] = data[key]

    return schema_and_values


async def get_entity_view(request: Request):
    try:
        # content
        entity: dict = await api.entity_get(request)

        # schema is e.g. person_1
        schema_name: str = entity["schema_name"].split("_")[0]
        schema_version = entity["schema_name"].split("_")[1]

        # schema
        schema = await api.schema_get_version(request, schema_name, schema_version)

        schema_and_values = _get_schema_and_values(schema, entity)

        context_values = {"title": translate("Entity"), "schema_and_values": schema_and_values}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("entities/entity.html", context)

    except Exception as e:
        raise HTTPException(404, detail=str(e), headers=None)
