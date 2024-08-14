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
    resource_type = request.path_params["resource_type"]

    context_variables = {"title": title, "resource": resource, "meta": resource["meta"]}
    context = await get_context(request, context_variables, resource_type)
    return context


async def get_resource(request: Request):
    resource_templates = {
        "collections": "resources/collections.html",
        "people": "resources/people.html",
        "locations": "resources/locations.html",
        "creators": "resources/creators.html",
        "events": "resources/events.html",
        "organisations": "resources/organisations.html",
        "collectors": "resources/collectors.html",
    }

    resource_type = request.path_params["resource_type"]
    if resource_type not in resource_templates:
        raise HTTPException(status_code=404, detail="Resource type not found")

    context = await _get_resource_context(request)
    template_path = resource_templates[resource_type]
    response = templates.TemplateResponse(request, template_path, context)
    return response


async def get_resopurce_json(request: Request):
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
