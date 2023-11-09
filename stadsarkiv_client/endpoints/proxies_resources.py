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
from stadsarkiv_client.core.hooks import get_hooks
import json


log = get_log()


async def _get_resource(request: Request):
    """
    Get resource from api and alter it with hooks
    """
    hooks = get_hooks(request)
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    resource = await api.proxies_get_resource(request, resource_type, id=id)
    resource = await hooks.after_get_resource(resource_type, resource)

    # remove leading zeros from id string
    # these ruins the search results
    id = id.lstrip("0")
    resource["id_real"] = id
    return resource


async def _get_collections_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    resource = resource_alter.collections_alter(resource)

    context_variables = {
        "title": title,
        "collection": resource,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/collections.html", context)


async def _get_people_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    people = resource_alter.people_alter(resource)

    context_variables = {
        "title": title,
        "people": people,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/people.html", context)


async def _get_locations_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    location = resource_alter.locations_alter(resource)

    context_variables = {
        "title": title,
        "location": location,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/locations.html", context)


async def _get_events_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    event = resource_alter.events_alter(resource)

    context_variables = {
        "title": title,
        "event": event,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/events.html", context)


async def _get_creators_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    creator = resource_alter.creators_alter(resource)

    context_variables = {
        "title": title,
        "creator": creator,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/creators.html", context)


async def _get_organisations_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    organisation = resource_alter.organisations_alter(resource)

    context_variables = {
        "title": title,
        "organisation": organisation,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/organisations.html", context)


async def _get_collectors_view(request: Request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    collector = resource_alter.collectors_alter(resource)

    context_variables = {
        "title": title,
        "collector": collector,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("resources/collectors.html", context)


async def get(request: Request):
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

    elif resource_type == "collectors":
        return await _get_collectors_view(request)

    raise HTTPException(status_code=404, detail="Resource type not found")


async def get_json(request: Request):
    id = request.path_params["id"]
    resource_type = request.path_params["resource_type"]
    collection = await api.proxies_get_resource(request, resource_type, id)
    collection_json = json.dumps(collection, indent=4, ensure_ascii=False)
    return PlainTextResponse(collection_json)
