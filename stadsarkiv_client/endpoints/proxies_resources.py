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
    resource["meta"]["title"] = title

    context_variables = {"title": title, "resource": resource, "meta": resource["meta"]}
    context = await get_context(request, context_variables)
    return context


async def get(request: Request):

    allow_resource_types = [
        "collections",
        "people",
        "locations",
        "creators",
        "events",
        "organisations",
        "collectors",
    ]

    resource_type = request.path_params["resource_type"]
    if resource_type not in allow_resource_types:
        raise HTTPException(status_code=404, detail="Resource type not found")

    context = await _get_resource_context(request)

    if resource_type == "collections":
        return templates.TemplateResponse(request, "resources/collections.html", context)

    elif resource_type == "people":
        return templates.TemplateResponse(request, "resources/people.html", context)

    elif resource_type == "locations":
        return templates.TemplateResponse(request, "resources/locations.html", context)

    elif resource_type == "creators":
        return templates.TemplateResponse(request, "resources/creators.html", context)

    elif resource_type == "events":
        return templates.TemplateResponse(request, "resources/events.html", context)

    elif resource_type == "organisations":
        return templates.TemplateResponse(request, "resources/organisations.html", context)

    elif resource_type == "collectors":
        return templates.TemplateResponse(request, "resources/collectors.html", context)


async def get_json(request: Request):
    id = request.path_params["id"]
    json_type = request.path_params["type"]
    resource_type = request.path_params["resource_type"]

    if json_type == "api":
        resource_api = await api.proxies_get_resource(request, resource_type, id)
        resource_json = json.dumps(resource_api, indent=4, ensure_ascii=False)
        return PlainTextResponse(resource_json)
    elif json_type == "resource_and_types":
        context = await _get_resource_context(request)
        resource_json = json.dumps(context["resource"], indent=4, ensure_ascii=False)
        return PlainTextResponse(resource_json)

    else:
        return HTTPException(status_code=404, detail="Type not found")
