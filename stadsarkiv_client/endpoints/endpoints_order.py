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
from stadsarkiv_client.database.crud_orders import database_orders
from stadsarkiv_client.database import utils_orders as utils
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.api import OpenAwsException

log = get_log()


async def _is_order_owner(request: Request, order_id: int) -> bool:
    """
    Check if user is authenticated and verified
    Check if user is owner of order
    """
    # await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)
    is_owner = await database_orders.is_owner_of_order(user_id=me["id"], order_id=order_id)
    return is_owner


async def _is_admin(request: Request) -> bool:
    """
    Check if user is authenticated and has required permissions to edit orders
    """
    return await api.has_permission(request, "employee")


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

    context_variables = {
        "title": "Bestil: " + meta_data["title"],
        "meta_title": "Bestil: " + meta_data["meta_title"],
        "meta_data": meta_data,
        "record_and_types": record_and_types,
        "is_active_by_user": await database_orders.is_record_active_by_user(
            user_id=me["id"],
            record_id=meta_data["id"],
        ),
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
        orders = await database_orders.get_orders_user(user_id=me["id"], completed=0)

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

    hooks = get_hooks(request)
    record_id = request.path_params["record_id"]

    record = await api.proxies_record_get_by_id(request, record_id)
    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    is_ordered = await database_orders.is_record_active_by_user(
        user_id=me["id"],
        record_id=meta_data["id"],
    )

    if not is_ordered:
        await database_orders.insert_order(meta_data, me)
        set_message(request, "Din bestilling er blevet oprettet", "success")
        return JSONResponse({"message": "Din bestilling er blevet oprettet", "error": False})
    else:
        return JSONResponse({"message": "Bestilling på dette materiale eksisterer allerede", "error": True})


async def orders_user_patch(request: Request):
    """
    User can only cancel their own order
    Admin can patch any order
    """
    await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)
    user_id = me["id"]

    order_id = request.path_params["order_id"]
    is_owner = await _is_order_owner(request, order_id)

    if not is_owner:
        return JSONResponse(
            {
                "message": "Du har ikke rettigheder til at opdatere denne bestilling",
                "error": True,
            }
        )

    filters = {"order_id": order_id}
    update_values = {"user_status": utils.STATUSES_USER.DELETED}

    await database_orders.update_order(update_values=update_values, filters=filters, user_id=user_id)
    return JSONResponse(
        {
            "message": "Din bestilling er blevet annuleret",
            "error": False,
        }
    )


async def orders_admin_patch(request: Request):
    """
    User can only cancel their own order
    Admin can patch any order
    """
    await is_authenticated_json(request, verified=True, permissions=["employee"])
    me = await api.users_me_get(request)

    is_admin = await _is_admin(request)
    if not is_admin:
        return JSONResponse(
            {
                "message": "Du har ikke rettigheder til at opdatere denne bestilling",
                "error": True,
            }
        )

    filters = {"order_id": request.path_params["order_id"]}
    update_values = await request.json()

    await database_orders.update_order(update_values=update_values, filters=filters, user_id=me["id"])

    return JSONResponse(
        {
            "message": "Bestillingemn er blevet annuleret",
            "error": False,
        }
    )


async def orders_admin_get(request: Request):
    """
    GET endpoint for displaying all orders for an employee
    """
    await is_authenticated(request, permissions=["employee"])

    orders = await database_orders.get_orders_admin(completed=0)

    context_values = {"title": "Bestillinger", "orders": orders}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/orders_admin.html", context)


async def orders_admin_get_edit(request: Request):
    """
    GET endpoint for displaying a single order for editing
    """
    await is_authenticated(request, permissions=["employee"])

    order_id = request.path_params["order_id"]
    order = await database_orders.get_order(order_id)

    context_values = {
        "title": "Opdater bestilling",
        "order": order,
        "locations": utils.STATUSES_ADMIN_HUMAN,
        "user_statuses": utils.STATUSES_USER_HUMAN,
    }
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/order_admin_edit.html", context)
