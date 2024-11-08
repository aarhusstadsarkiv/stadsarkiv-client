from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import api
from stadsarkiv_client.core.auth import is_authenticated, is_authenticated_json
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.database import orders
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.flash import set_message
import json

log = get_log()


async def orders_get_order(request: Request):
    await is_authenticated(request, verified=True)
    me = await api.users_me_get(request)

    hooks = get_hooks(request)
    record_id = request.path_params["record_id"]

    record = await api.proxies_record_get_by_id(request, record_id)
    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    record_altered = record_alter.record_alter(request, record, meta_data)
    record_and_types = record_alter.get_record_and_types(record_altered)

    filters = {
        "user_id": me["id"],
        "record_id": meta_data["id"],
    }

    context_variables = {
        "title": "Bestil: " + meta_data["title"],
        "meta_title": "Bestil: " + meta_data["meta_title"],
        "meta_data": meta_data,
        "record_and_types": record_and_types,
        "is_ordered": await orders.orders_exists(filters),
    }

    context = await get_context(request, context_values=context_variables)

    return templates.TemplateResponse(request, "order/order.html", context)


def _get_insert_data(meta_data: dict, me: dict):
    return {
        "user_id": me["id"],
        "record_id": meta_data["id"],
        "resources": json.dumps(meta_data["resources"]),
        # "barcode": meta_data["barcode"],
        # "storage_id": meta_data["storage_id"],
        # "location": meta_data["location"],
        "label": meta_data["title"],
    }


async def orders_post(request: Request):
    await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)

    hooks = get_hooks(request)
    record_id = request.path_params["record_id"]

    record = await api.proxies_record_get_by_id(request, record_id)
    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    filters = {
        "user_id": me["id"],
        "record_id": meta_data["id"],
    }

    if not await orders.orders_exists(filters):
        data = _get_insert_data(meta_data, me)
        await orders.orders_insert(data)
        set_message(request, "Din bestilling er blevet oprettet", "success")
        return JSONResponse({"message": "Din bestilling er blevet oprettet", "error": False})
    else:
        return JSONResponse({"message": "Bestilling på dette materiale eksisterer allerede", "error": True})


"""
Proxy for search records endpoints


http://localhost:5555/records/000503354
identifikation: "51648293"

http://localhost:5555/records/000504168
storage_id: ['91+01390-2']

000429798

(None, '8038476141', 'Reol 106/fag 2/hylde 1')

000506083

(['91+01418-1'], None, None)


"""
