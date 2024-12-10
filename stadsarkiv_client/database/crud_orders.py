"""
A collection of functions for performing CRUD operations on orders.
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.database import utils_orders
from stadsarkiv_client.database.utils import DatabaseConnection
from stadsarkiv_client.core.logging import get_log
import json


log = get_log()

try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""


async def _has_active_order(crud: "CRUD", user_id: str, record_id: str):
    """
    Check if user has an active order on a record
    """
    statuses = [utils_orders.STATUSES_USER.ORDERED, utils_orders.STATUSES_USER.QUEUED]
    order = await _get_orders_one(crud, statuses, record_id, user_id)
    return order


async def has_active_order(user_id: str, record_id: str):
    """
    Check if user has an active order on a record
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        is_active = await _has_active_order(crud, user_id, record_id)
    return is_active


async def is_owner(user_id: str, order_id: int):
    """
    Check if user is owner of order
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        filters = {"order_id": order_id, "user_id": user_id}
        is_owner = await crud.exists(
            table="orders",
            filters=filters,
        )

    return is_owner


async def insert_order(meta_data: dict, me: dict):
    """
    Insert order into database
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        is_active_by_user = await _has_active_order(crud, me["id"], meta_data["id"])
        if is_active_by_user:
            # This may happen is user has already ordered the record
            # In reality it will only happen if the user has two tabs open and POST the same order twice
            raise Exception("User is already active on this record")

        # insert or update user
        user_insert_update_values = utils_orders.get_insert_user_data(me)
        await crud.replace("users", user_insert_update_values, {"user_id": me["id"]})

        # Check if record is already in database
        # But location is not updated if record already exists
        record = await crud.select_one("records", filters={"record_id": meta_data["id"]})
        if record:
            record_insert_update_values = utils_orders.get_insert_record_data(meta_data, record["location"])
        else:
            record_insert_update_values = utils_orders.get_insert_record_data(meta_data)

        # Insert or update record
        await crud.replace("records", record_insert_update_values, {"record_id": meta_data["id"]})

        # Check if active order exists on record.
        # If so, set status to QUEUED, otherwise set status to ORDERED
        active_order = await _get_orders_one(crud, [utils_orders.STATUSES_USER.ORDERED], meta_data["id"])
        if active_order:
            user_status = utils_orders.STATUSES_USER.QUEUED
        else:
            user_status = utils_orders.STATUSES_USER.ORDERED

        await crud.insert(
            "orders",
            utils_orders.get_order_data(
                user_insert_update_values["user_id"],
                record_insert_update_values["record_id"],
                user_status,
            ),
        )

        last_order_id = await crud.last_insert_id()
        order_data = await crud.select_one("orders", filters={"order_id": last_order_id})

        # Insert log message
        await _insert_log_message(
            crud,
            order_id=order_data["order_id"],
            location=record_insert_update_values["location"],
            user_status=order_data["user_status"],
            changed_by=me["id"],
        )

        # If location is reading room then send message to user
        if record_insert_update_values["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM:
            deadline_date = utils_orders.get_deadline_date()
            order_data["deadline"] = deadline_date

            # Set order deadline and message_sent to 1
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date, "message_sent": 1},
                filters={"order_id": order_data["order_id"]},
            )

            utils_orders.send_order_message("Order moved to reading room.", order_data)


async def _on_user_status_change(crud: "CRUD", order_id: str, new_user_status: int):
    """
    Possible statuses. If order is COMPLETED or DELETED then check if there are QUEUED orders on the record.
    Select first QUEUED order and alter status to ORDERED.
    """
    order = await _get_orders_one(crud, order_id=order_id)
    if new_user_status in [utils_orders.STATUSES_USER.COMPLETED, utils_orders.STATUSES_USER.DELETED]:
        next_queued_order = await _get_orders_one(crud, [utils_orders.STATUSES_USER.QUEUED], order["record_id"])
        if next_queued_order:
            await crud.update(
                table="orders",
                update_values={"user_status": utils_orders.STATUSES_USER.ORDERED},
                filters={"order_id": next_queued_order["order_id"]},
            )
            log.debug(f"Order {next_queued_order['order_id']} status changed to ORDERED")

            # Check is location is 'reading room'
            # If so, send message to user notifying that the order is ready in the reading room
            if next_queued_order["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM:

                # Set order deadline and message_sent to 1
                deadline_date = utils_orders.get_deadline_date()
                await crud.update(
                    table="orders",
                    update_values={"deadline": deadline_date, "message_sent": 1},
                    filters={"order_id": next_queued_order["order_id"]},
                )

                utils_orders.send_order_message("Order moved to reading room.", next_queued_order)


async def _on_location_change(crud: "CRUD", new_location: int, order_id: str):

    # If location is 0 then do nothing
    if not new_location:
        return

    old_order = await _get_orders_one(crud, order_id=order_id)
    await crud.update(
        table="records",
        update_values={"location": new_location},
        filters={"record_id": old_order["record_id"]},
    )

    # Get updated order
    updated_order = await _get_orders_one(crud, order_id=order_id)
    if old_order["location"] != new_location:

        # New location is reading room
        if new_location == utils_orders.STATUSES_LOCATION.READING_ROOM:
            deadline_date = utils_orders.get_deadline_date()

            # Update deadline on order
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date},
                filters={"order_id": order_id},
            )

            # set message_sent to 1 on order
            await crud.update(
                table="orders",
                update_values={"message_sent": 1},
                filters={"order_id": order_id},
            )

            # Send message to user if not already sent
            if not old_order["message_sent"]:
                updated_order["deadline"] = deadline_date
                utils_orders.send_order_message("Order moved to reading room.", updated_order)


async def _allow_location_change(crud: "CRUD", record_id: str):
    """
    Check if location can be changed
    Get orders where location is READING_ROOM and user_status is ORDERED
    If there are no orders then location can be changed
    """
    orders = await _get_orders(
        crud,
        [utils_orders.STATUSES_USER.ORDERED],
        location=utils_orders.STATUSES_LOCATION.READING_ROOM,
        record_id=record_id,
    )
    if orders:
        return False
    return True


async def update_order(location: int, update_values: dict, order_id: str, user_id: str):
    """
    Update order by order_id. Allow to set values of order and record.
    Update order: user_status, deadline, comment, record: location
    """

    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        filters = {"order_id": order_id}
        if update_values:
            await crud.update(
                table="orders",
                update_values=update_values,
                filters=filters,
            )

        # Either location is changed or user_status is changed, not both
        await _on_location_change(crud, location, order_id)

        updated_order = await _get_orders_one(crud, order_id=order_id)
        await _on_user_status_change(crud, order_id, updated_order["user_status"])

        # Insert log message
        await _insert_log_message(
            crud,
            order_id=order_id,
            location=updated_order["location"],
            user_status=updated_order["user_status"],
            changed_by=user_id,
        )


async def get_orders_user(user_id: str, completed=0):
    """
    Get all orders for a user. Exclude orders with specific statuses.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        if completed:
            orders = await _get_orders(
                crud,
                [utils_orders.STATUSES_USER.COMPLETED],
                user_id=user_id,
            )
        else:
            orders = await _get_orders(
                crud,
                [utils_orders.STATUSES_USER.ORDERED, utils_orders.STATUSES_USER.QUEUED],
                user_id=user_id,
            )

        for order in orders:
            order = format_order_for_display(order)

        return orders


async def _get_orders_query_params(
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: str = "",
    location: int = 0,
    group_by: str = "",
):
    """
    SELECT complete order data by statuses, record_id, user_id, order_id
    Returns query and params
    """
    where_clauses = []
    params: dict = {}

    if statuses:
        statuses_str = ", ".join([str(status) for status in statuses])
        where_clauses.append(f"o.user_status IN ({statuses_str})")

    if record_id:
        where_clauses.append("r.record_id = :record_id")
        params["record_id"] = record_id

    if user_id:
        where_clauses.append("o.user_id = :user_id")
        params["user_id"] = user_id

    if order_id:
        where_clauses.append("o.order_id = :order_id")
        params["order_id"] = order_id

    if location:
        where_clauses.append("r.location = :location")
        params["location"] = location

    query = """
    SELECT * FROM orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    """

    if where_clauses:
        query += "WHERE " + " AND ".join(where_clauses) + " "

    if group_by:
        query += f"GROUP BY {group_by} "

    query += "ORDER BY o.order_id DESC"
    return query, params


async def _get_orders(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: str = "",
    location: int = 0,
    group_by: str = "",
):
    query, params = await _get_orders_query_params(statuses, record_id, user_id, order_id, location, group_by )

    return await crud.query(query, params)


async def _get_orders_one(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: str = "",
    location: int = 0,
):
    """
    Get orders by statuses, record_id, user_id and order_id
    """
    query, params = await _get_orders_query_params(statuses, record_id, user_id, order_id, location)
    order = await crud.query_one(query, params)
    return order


async def get_orders_admin(status: str = "active"):
    """
    Get all orders for a user. Allow to set status and finished.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        if status == "active":
            orders = await _get_orders(crud, [utils_orders.STATUSES_USER.ORDERED, utils_orders.STATUSES_USER.QUEUED])
        elif status == "completed":
            orders = await _get_orders(crud, [utils_orders.STATUSES_USER.COMPLETED], group_by="o.record_id")

        for order in orders:
            order = utils_orders.format_order_display(order)

            # Only if order has status ORDERED then check if there are queued orders
            if order["user_status"] == utils_orders.STATUSES_USER.ORDERED:
                queued_orders = await _get_orders(crud, [utils_orders.STATUSES_USER.QUEUED], order["record_id"])
                order["count"] = len(queued_orders)
            else:
                order["count"] = 0

            if order["user_status"] == utils_orders.STATUSES_USER.COMPLETED:
                order["actions_deactivated"] = True

            log.debug(f"Order: {order}")

        return orders


async def get_order(order_id):
    """
    Get a single joined order by order_id for display on the admin edit order page
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        order = await _get_orders_one(CRUD(connection), order_id=order_id)
        order = format_order_for_display(order)
        allow_location_change = await _allow_location_change(CRUD(connection), order["record_id"])
        order["allow_location_change"] = allow_location_change
        log.debug(f"Order: {order}")
        return order


def format_order_for_display(order: dict):
    """
    Format order for display
    """
    order["resources"] = json.loads(order["resources"])
    order = utils_orders.format_order_display(order)
    return order


async def _insert_log_message(crud: "CRUD", order_id, location, user_status, changed_by):
    log_message = {
        "order_id": order_id,
        "location": location,
        "user_status": user_status,
        "changed_by": changed_by,
    }

    await crud.insert("orders_log", log_message)
