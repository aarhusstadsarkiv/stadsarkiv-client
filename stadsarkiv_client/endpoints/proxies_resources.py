from starlette.requests import Request
from starlette.responses import PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json

from stadsarkiv_client.resources import collections_alter


log = get_log()


async def get_collections_view(request: Request):
    collection_id = request.path_params["collection_id"]
    collection = await api.proxies_entity_by_type("collections", collection_id=collection_id)
    collection = collections_alter.collections_alter(collection)
    collection["id"] = collection_id
    context_variables = {
        "title": collection["display_label"],
        "collection": collection,
    }

    context = await get_context(request, context_variables)
    return templates.TemplateResponse("records/collections.html", context)


async def get_collections_view_json(request: Request):
    collection_id = request.path_params["collection_id"]
    collection = await api.proxies_collection(collection_id=collection_id)
    collection = collections_alter.collections_alter(collection)
    collection_json = json.dumps(collection, indent=4, ensure_ascii=False)
    return PlainTextResponse(collection_json)
