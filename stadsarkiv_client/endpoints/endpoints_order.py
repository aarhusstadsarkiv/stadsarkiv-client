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
from stadsarkiv_client.core import date_format
import json

log = get_log()


async def orders_get_order(request: Request):
    """
    GET page when user wants to order a record
    User needs to be authenticated and verified
    """
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


async def orders_get_orders(request: Request):
    """
    GET endpoint for displaying all orders for authenticated user
    """
    await is_authenticated(request, permissions=["employee"])
    try:

        me = await api.users_me_get(request)
        orders_me = await crud_orders.select(
            filters={"user_id": me["id"], "done": 0},
            order_by=[("created_at", "DESC")],
        )

        context_values = {"title": translate("Your orders"), "me": me, "orders": orders_me}
        context = await get_context(request, context_values=context_values)

        return templates.TemplateResponse(request, "order/orders_user.html", context)
    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception("Error in auth_orders")
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def orders_post(request: Request):
    """
    POST endpoint for creating an order
    """
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


async def orders_patch(request: Request):
    """
    User can only cancel their own orders
    """

    await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)
    order_id = request.path_params["order_id"]

    filters = {
        "user_id": me["id"],
        "id": order_id,
    }

    is_owner = await crud_orders.owns(id=order_id, user_id=me["id"])
    if not is_owner:
        return JSONResponse(
            {
                "message": "Du har ikke rettigheder til at annullere denne bestilling",
                "error": True,
            }
        )

    filters = {"id": order_id}
    update_values = {"done": 1, "status": "ORDERED"}

    await crud_orders.order_patch_user(update_values=update_values, filters=filters)
    return JSONResponse(
        {
            "message": "Din bestilling er blevet annuleret",
            "error": False,
        }
    )


async def orders_admin_get(request: Request):
    """
    GET endpoint for displaying all orders
    """
    await is_authenticated(request, permissions=["employee"])

    orders = await crud_orders.select(order_by=[("id", "DESC")])
    for order in orders:
        order["resources"] = json.loads(order["resources"])
        order = _date_format_order(order)

    user = await api.user_get_by_uuid(request, order["user_id"])

    context_values = {"title": "Bestillinger", "orders": orders, "user": user}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/admin_orders.html", context)


async def orders_admin_get_edit(request: Request):
    """
    GET endpoint for displaying a single order for editing
    """
    await is_authenticated(request, permissions=["employee"])

    order_id = request.path_params["order_id"]
    order = await crud_orders.select_one(filters={"id": order_id})
    order["resources"] = json.loads(order["resources"])
    order = _date_format_order(order)

    context_values = {"order": order}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/order_edit.html", context)


def _get_insert_data(meta_data: dict, me: dict):
    """
    Generate data for inserting into orders table
    """
    return {
        "user_id": me["id"],
        "user_email": me["email"],
        "user_display_name": me["display_name"],
        "record_id": meta_data["id"],
        "resources": json.dumps(meta_data["resources"]),
        "label": meta_data["title"],
    }


def _date_format_order(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    order["created_at"] = date_format.timezone_alter(order["created_at"])
    order["modified_at"] = date_format.timezone_alter(order["modified_at"])
    if order["deadline"]:
        order["deadline"] = date_format.timezone_alter(order["deadline"])
    return order


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
