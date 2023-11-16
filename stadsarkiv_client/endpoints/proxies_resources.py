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


async def _get_resource_context(request):
    resource = await _get_resource(request)
    title = resource["display_label"]
    resource = resource_alter.resource_alter(resource)

    context_variables = {
        "title": title,
        "resource": resource,
    }

    context = await get_context(request, context_variables)
    return context


async def get(request: Request):
    resource_type = request.path_params["resource_type"]

    context = await _get_resource_context(request)

    if resource_type == "collections":
        return templates.TemplateResponse("resources/collections.html", context)

    elif resource_type == "people":
        return templates.TemplateResponse("resources/people.html", context)

    elif resource_type == "locations":
        return templates.TemplateResponse("resources/locations.html", context)

    elif resource_type == "creators":
        return templates.TemplateResponse("resources/creators.html", context)

    elif resource_type == "events":
        return templates.TemplateResponse("resources/events.html", context)

    elif resource_type == "organisations":
        return templates.TemplateResponse("resources/organisations.html", context)

    elif resource_type == "collectors":
        return templates.TemplateResponse("resources/collectors.html", context)

    raise HTTPException(status_code=404, detail="Resource type not found")


async def get_json(request: Request):
    id = request.path_params["id"]
    type = request.path_params["type"]

    if type == "api":
        resource_type = request.path_params["resource_type"]
        collection = await api.proxies_get_resource(request, resource_type, id)
        collection_json = json.dumps(collection, indent=4, ensure_ascii=False)
        return PlainTextResponse(collection_json)
