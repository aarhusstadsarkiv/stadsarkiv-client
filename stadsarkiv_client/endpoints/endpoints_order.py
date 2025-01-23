from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import api
from stadsarkiv_client.core.auth import is_authenticated, is_authenticated_json
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database import crud_orders
from stadsarkiv_client.database import utils_orders
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.endpoints.endpoints_utils import get_record_data

from starlette.requests import Request

from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
from stadsarkiv_client.endpoints.endpoints_utils import get_record_data
from stadsarkiv_client.core import utils_core



log = get_log()


async def _is_order_owner(request: Request, order_id: int) -> bool:
    """
    Check if user is authenticated and verified
    Check if user is owner of order
    """
    me = await api.users_me_get(request)
    is_owner = await crud_orders.is_owner(user_id=me["id"], order_id=order_id)
    return is_owner


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
    permissions = await api.me_permissions(request)

    try:
        record_id = request.path_params["record_id"]

        record = await api.proxies_record_get_by_id(record_id)
        record, meta_data, record_and_types = await get_record_data(request, record, permissions)

        is_ordered = await crud_orders.has_active_order(
            user_id=me["id"],
            record_id=meta_data["id"],
        )

        if is_ordered:
            return JSONResponse({"message": "Bestilling på dette materiale eksisterer allerede", "error": True})
        else:
            await crud_orders.insert_order(meta_data, record_and_types, me)
            return JSONResponse({"message": "Din bestilling er blevet oprettet", "error": False})
    except Exception as e:
        log.exception("Error in auth_orders_post")
        return JSONResponse({"message": str(e), "error": True})


async def _process_order_deletion(request: Request, id_key: str):
    """
    This mehtod is used to delete an order based on the provided key (e.g., "order_id" or "record_id")
    There is two options because the user can delete an order based on the order_id or the record_id
    """
    await is_authenticated_json(request, verified=True)
    me = await api.users_me_get(request)

    try:
        user_id = me["id"]

        # Get the order_id based on the provided key
        target_id = request.path_params[id_key]
        if id_key == "record_id":
            order = await crud_orders.get_order_by_record_id(user_id, target_id)
            order_id = order["order_id"]
        else:
            order_id = target_id

        # Check if user is the owner of the order
        is_owner = await _is_order_owner(request, order_id)
        if not is_owner:
            return JSONResponse(
                {
                    "message": "Du har ikke rettigheder til at opdatere denne bestilling",
                    "error": True,
                }
            )

        # Update the order with the status. Location is not altered, hence it is set to 0
        update_values = {
            "user_status": utils_orders.STATUSES_USER.DELETED,
        }

        await crud_orders.update_order(
            location=0,
            update_values=update_values,
            order_id=order_id,
            user_id=user_id,
        )

    except Exception:
        log.exception("Error in orders_user_delete")
        return JSONResponse({"message": "Der opstod en fejl. Bestilling kunne ikke slettes.", "error": True})

    return JSONResponse({"message": "Din bestilling er slettet", "error": False})


async def orders_user_patch(request: Request):
    return await _process_order_deletion(request, id_key="order_id")


async def orders_user_delete(request: Request):
    return await _process_order_deletion(request, id_key="record_id")


async def _get_location(update_values: dict) -> int:
    """
    Get location from a dict of update values and remove it from update_values
    """
    location = 0
    if "location" in update_values:
        location = int(update_values["location"])
        update_values.pop("location")
    return location


async def orders_admin_patch(request: Request):
    """
    Patch multiple orders at once
    """
    try:
        await is_authenticated_json(request, verified=True, permissions=["employee"])
        me = await api.users_me_get(request)

        # Mutiple orders can be updated at once
        update_values: list = await request.json()
        num_orders = len(update_values)
        for update_value in update_values:
            order_id = update_value["order_id"]
            location = await _get_location(update_value)
            await crud_orders.update_order(
                location=location,
                update_values=update_value,
                order_id=order_id,
                user_id=me["id"],
            )

        if len(update_values) == 1:
            flash.set_message(request, "1 bestilling er blevet opdateret", type="success")
        elif len(update_values) > 1:
            flash.set_message(request, f"{num_orders} bestillinger er blevet opdateret", type="success")
        else:
            flash.set_message(request, "Ingen lokationer blev opdateret", type="success")
        return JSONResponse({"error": False})
    except Exception as e:
        flash.set_message(request, str(e), type="error")
        log.exception("Error in orders_admin_patch_location")
        return JSONResponse({"error": True})


async def orders_admin_patch_single(request: Request):
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
                "error": False,
            }
        )
    except Exception:
        log.exception("Error in orders_admin_patch")
        return JSONResponse(
            {
                "error": True,
            }
        )


async def orders_admin_get(request: Request):
    """
    GET endpoint for displaying all orders for an employee
    """
    await is_authenticated(request, permissions=["employee"])
    me = await api.users_me_get(request)
    await crud_orders.replace_employee(me)

    # get status from query params
    filter_status = request.query_params.get("filter_status", "active")
    filter_location = request.query_params.get("filter_location", "all")
    if filter_location == "all":
        filter_location = ""
    filter_email = request.query_params.get("filter_email", "")
    filter_user = request.query_params.get("filter_user", "")

    orders = await crud_orders.get_orders_admin(
        filter_status=filter_status,
        filter_location=filter_location,
        filter_email=filter_email,
        filter_user=filter_user,
    )

    context_values = {
        "title": "Bestillinger",
        "orders": orders,
        "filter_status": filter_status,
        "filter_location": filter_location,
        "filter_email": filter_email,
        "filter_user": filter_user,
        "locations": utils_orders.STATUSES_LOCATION_HUMAN,
    }
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, "order/orders_admin.html", context)


async def orders_admin_get_edit(request: Request):
    """
    GET endpoint for displaying a single order for editing
    """
    await is_authenticated(request, permissions=["employee"])

    order_id = request.path_params["order_id"]
    order = await crud_orders.get_order(order_id)

    log.debug(order)

    context_values = {
        "title": "Opdater bestilling",
        "order": order,
        "locations": utils_orders.STATUSES_LOCATION_HUMAN,
        "user_statuses": utils_orders.STATUSES_USER_HUMAN,
    }
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "order/order_admin_edit.html", context)


async def orders_record_get(request: Request):
    """
    Simple display of a record
    """
    await is_authenticated(request, permissions=["employee"])

    record_id = request.path_params["record_id"]
    permissions = await api.me_permissions(request)
    record = await api.proxies_record_get_by_id(record_id)

    record, meta_data, record_and_types = await get_record_data(request, record, permissions)    
    all_keys = list(record_and_types.keys())
    all_keys = ["collectors", "resources", "subjects", "date_normalized", "desc_notes"]
    html = utils_core.get_parsed_data_as_table(record_and_types, all_keys, debug=True)
    context_variables = {
        "html": html,
        "title": meta_data["title"],
        "meta_title": meta_data["meta_title"],
        "meta_description": meta_data["meta_description"],
        "record_id": record_id,
    }

    context = await get_context(request, context_variables, "record")
    return templates.TemplateResponse(request, "order/orders_record.html", context)


async def orders_logs(request: Request):
    await is_authenticated(request, permissions=["employee"])

    logs = await crud_orders.get_logs()
    context_variables = {
        "logs": logs,
        "title": "Order Logs",
        "meta_title": "Order Logs",
    }

    context = await get_context(request, context_variables, "record")
    return templates.TemplateResponse(request, "order/orders_logs.html", context)
