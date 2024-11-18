from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import api
from stadsarkiv_client.core.auth import is_authenticated, is_authenticated_json
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.flash import set_message
from stadsarkiv_client.database.orders import crud_orders
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.api import OpenAwsException

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
        "is_ordered": await crud_orders.exists(filters),
    }

    context = await get_context(request, context_values=context_variables)

    return templates.TemplateResponse(request, "order/order.html", context)


def _get_insert_data(meta_data: dict, me: dict):
    return {
        "user_id": me["id"],
        "record_id": meta_data["id"],
        "resources": json.dumps(meta_data["resources"]),
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

    if not await crud_orders.exists(filters):
        data = _get_insert_data(meta_data, me)
        await crud_orders.insert(data)
        set_message(request, "Din bestilling er blevet oprettet", "success")
        return JSONResponse({"message": "Din bestilling er blevet oprettet", "error": False})
    else:
        return JSONResponse({"message": "Bestilling på dette materiale eksisterer allerede", "error": True})


async def admin_orders_get(request: Request):
    await is_authenticated(request, permissions=["employee"])

    orders = await crud_orders.select(order_by=[("id", "DESC")])
    orders = [dict(order) for order in orders]

    for order in orders:
        order["resources"] = json.loads(order["resources"])

    context_values = {"title": "Bestillinger", "orders": orders}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/admin_orders.html", context)


async def auth_orders(request: Request):
    await is_authenticated(request)
    try:

        me = await api.users_me_get(request)
        orders_me = await crud_orders.select(
            filters={"user_id": me["id"]},
            order_by=[("created_at", "DESC")],
        )

        context_values = {"title": translate("Your orders"), "me": me, "orders": orders_me}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "auth/orders.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception("Error in auth_orders")
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


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
