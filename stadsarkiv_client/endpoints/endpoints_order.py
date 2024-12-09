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
from stadsarkiv_client.database import crud_orders
from stadsarkiv_client.database import utils_orders
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.api import OpenAwsException

log = get_log()


async def _is_order_owner(request: Request, order_id: int) -> bool:
    """
    Check if user is authenticated and verified
    Check if user is owner of order
    """
    me = await api.users_me_get(request)
    is_owner = await crud_orders.is_owner(user_id=me["id"], order_id=order_id)
    return is_owner


async def orders_get_order(request: Request):
    """
    GET Page where user can order a record
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

    is_active_by_user = await crud_orders.has_active_order(
        user_id=me["id"],
        record_id=meta_data["id"],
    )

    context_variables = {
        "title": "Bestil: " + meta_data["title"],
        "meta_title": "Bestil: " + meta_data["meta_title"],
        "meta_data": meta_data,
        "record_and_types": record_and_types,
        "is_active_by_user": is_active_by_user,
    }

    context = await get_context(request, context_values=context_variables)
    return templates.TemplateResponse(request, "order/order.html", context)


async def orders_get_orders(request: Request):
    """
    GET endpoint for displaying all orders for authenticated user
    """
    await is_authenticated(request, verified=True)
    try:

        me = await api.users_me_get(request)
        orders = await crud_orders.get_orders_user(user_id=me["id"], completed=0)

        context_values = {"title": translate("Your orders"), "me": me, "orders": orders}
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

    try:
        hooks = get_hooks(request)
        record_id = request.path_params["record_id"]

        record = await api.proxies_record_get_by_id(request, record_id)
        meta_data = get_record_meta_data(request, record)
        record, meta_data = await hooks.after_get_record(record, meta_data)

        is_ordered = await crud_orders.has_active_order(
            user_id=me["id"],
            record_id=meta_data["id"],
        )

        if not is_ordered:
            await crud_orders.insert_order(meta_data, me)
            set_message(request, "Din bestilling er blevet oprettet", "success")
            return JSONResponse({"message": "Din bestilling er blevet oprettet", "error": False})
        else:
            return JSONResponse({"message": "Bestilling på dette materiale eksisterer allerede", "error": True})
    except Exception as e:
        log.exception("Error in auth_orders_post")
        return JSONResponse({"message": str(e), "error": True})


async def orders_user_patch(request: Request):
    """
    User can only cancel their own order
    Admin can patch any order
    """
    await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)
    user_id = me["id"]

    # Check if user is owner of order
    order_id = request.path_params["order_id"]
    is_owner = await _is_order_owner(request, order_id)

    if not is_owner:
        return JSONResponse(
            {
                "message": "Du har ikke rettigheder til at opdatere denne bestilling",
                "error": True,
            }
        )

    update_values = {"user_status": utils_orders.STATUSES_USER.DELETED}

    # User can not alter location, only admin can, therefor location is set to 0
    await crud_orders.update_order(location=0, update_values=update_values, order_id=order_id, user_id=user_id)
    flash.set_message(request, "Din bestilling er slettet", type="success")

    return JSONResponse({"error": False})


async def _get_location(update_values: dict) -> int:
    """
    Get location from a dict of update values and remove it from update_values
    """
    location = 0
    if "location" in update_values:
        location = update_values["location"]
        update_values.pop("location")
    return location


async def orders_admin_patch(request: Request):
    """
    User can only cancel their own order
    Admin can patch any order
    """
    try:
        await is_authenticated_json(request, verified=True, permissions=["employee"])
        me = await api.users_me_get(request)

        order_id = request.path_params["order_id"]
        update_values: dict = await request.json()

        location = await _get_location(update_values)

        await crud_orders.update_order(
            location=location,
            update_values=update_values,
            order_id=order_id,
            user_id=me["id"],
        )

        if update_values.get("user_status") == utils_orders.STATUSES_USER.DELETED:
            message = "Din bestilling er blevet slettet"
        else:
            message = "Bestillingen er blevet opdateret"

        flash.set_message(request, message, type="success")
        return JSONResponse(
            {
                "message": message,
                "error": False,
            }
        )
    except Exception as e:
        log.exception("Error in orders_admin_patch")
        return JSONResponse({"message": str(e), "error": True})


async def orders_admin_get(request: Request):
    """
    GET endpoint for displaying all orders for an employee
    """
    await is_authenticated(request, permissions=["employee"])

    orders = await crud_orders.get_orders_admin(completed=0)

    context_values = {"title": "Bestillinger", "orders": orders}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/orders_admin.html", context)


async def orders_admin_get_edit(request: Request):
    """
    GET endpoint for displaying a single order for editing
    """
    await is_authenticated(request, permissions=["employee"])

    order_id = request.path_params["order_id"]
    order = await crud_orders.get_order(order_id)

    context_values = {
        "title": "Opdater bestilling",
        "order": order,
        "locations": utils_orders.STATUSES_LOCATION_HUMAN,
        "user_statuses": utils_orders.STATUSES_USER_HUMAN,
    }
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "order/order_admin_edit.html", context)
