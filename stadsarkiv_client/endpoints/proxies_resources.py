"""
Proxy for resources endpoints
- locations
- people
- collections
(etc)

All that is not records
"""

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.resources import resource_alter
import json

log = get_log()


async def _get_collections_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    collection = await api.proxies_entity_by_type(resource_type, id=id)
    collection["id_real"] = id
    title = collection["display_label"]
    collection = resource_alter.collections_alter(collection)

    context_variables = {
        "title": title,
        "collection": collection,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/collections.html", context)


async def _get_people_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    people = await api.proxies_entity_by_type(resource_type, id=id)
    people["id_real"] = id
    title = people["display_label"]
    people = resource_alter.people_alter(people)
    context_variables = {
        "title": title,
        "people": people,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/people.html", context)


async def _get_locations_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]

    location = await api.proxies_entity_by_type(resource_type, id=id)
    title = location["display_label"]
    location["id_real"] = id
    location = resource_alter.locations_alter(location)
    context_variables = {
        "title": title,
        "location": location,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/locations.html", context)


async def _get_events_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]

    event = await api.proxies_entity_by_type(resource_type, id=id)
    title = event["display_label"]
    event["id_real"] = id
    event = resource_alter.events_alter(event)

    log.debug(event)
    context_variables = {
        "title": title,
        "event": event,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/events.html", context)


async def _get_creators_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]

    creator = await api.proxies_entity_by_type(resource_type, id=id)
    title = creator["display_label"]
    creator["id_real"] = id
    creator = resource_alter.creators_alter(creator)

    context_variables = {
        "title": title,
        "creator": creator,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/creators.html", context)


async def _get_organisations_view(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]

    organisation = await api.proxies_entity_by_type(resource_type, id=id)
    title = organisation["display_label"]
    organisation["id_real"] = id
    organisation = resource_alter.creators_alter(organisation)

    context_variables = {
        "title": title,
        "organisation": organisation,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/organisations.html", context)


async def get_resources_view(request: Request):
    resource_type = request.path_params["resource_type"]

    if resource_type == "collections":
        return await _get_collections_view(request)

    elif resource_type == "people":
        return await _get_people_view(request)

    elif resource_type == "locations":
        return await _get_locations_view(request)

    elif resource_type == "creators":
        return await _get_creators_view(request)

    elif resource_type == "events":
        return await _get_events_view(request)

    elif resource_type == "organisations":
        return await _get_organisations_view(request)

    raise HTTPException(status_code=404, detail="Resource type not found")


async def get_resources_view_json(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    collection = await api.proxies_entity_by_type(resource_type, id)
    collection_json = json.dumps(collection, indent=4, ensure_ascii=False)
    return PlainTextResponse(collection_json)
