from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.resources import collections_alter
import json

log = get_log()

resource_types = ["creators", "people", "places", "collections"]


async def _get_collections_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    collection = await api.proxies_entity_by_type(resource_type, id=id)
    collection = collections_alter.collections_alter(collection)
    collection["id"] = id
    context_variables = {
        "title": collection["display_label"],
        "collection": collection,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/collections.html", context)


async def _get_people_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    people = await api.proxies_entity_by_type(resource_type, id=id)
    people = collections_alter.collections_alter(people)
    people["id"] = people
    context_variables = {
        "title": people["display_label"],
        "data": people,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/collections.html", context)


async def get_resources_view(request: Request):
    # id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]

    if resource_type not in resource_types:
        raise HTTPException(status_code=404, detail="Resource type not found")

    if resource_type == "collections":
        return await _get_collections_view(request)

    if resource_type == "people":
        return await _get_people_view(request)


async def get_collections_view_json(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    collection = await api.proxies_entity_by_type(resource_type, id)
    collection_json = json.dumps(collection, indent=4, ensure_ascii=False)
    return PlainTextResponse(collection_json)
