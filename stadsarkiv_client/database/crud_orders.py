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

        # Check if user is already active on this record
        is_active_by_user = await _has_active_order(crud, me["id"], meta_data["id"])
        if is_active_by_user:
            # This may happen is user has already ordered the record
            # In reality it will only happen if the user has two tabs open and POST the same order twice
            raise Exception("User is already active on this record")

        # insert or update user
        user_insert_update_values = utils_orders.get_insert_user_data(me)
        await crud.replace("users", user_insert_update_values, {"user_id": me["id"]})

        # insert or update record
        record_insert_update_values = utils_orders.get_insert_record_data(meta_data)
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

        # Send message to user
        utils_orders.send_order_message("Order created", order_data)

        # Insert log message
        await _insert_log_message(
            crud,
            order_id=order_data["order_id"],
            location=record_insert_update_values["location"],
            user_status=order_data["user_status"],
            changed_by=me["id"],
        )


async def update_order(location: int, update_values: dict, filters: dict, user_id: str):
    """
    Update order by order_id. Allow to set any values in the order and location of the record.
    """

    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        if update_values:
            await crud.update(
                table="orders",
                update_values=update_values,
                filters=filters,
            )

        updated_order = await _get_orders_one(crud, order_id=filters["order_id"])

        if location:
            await crud.update(
                table="records",
                update_values={"location": location},
                filters={"record_id": updated_order["record_id"]},
            )

        # Send message to user
        utils_orders.send_order_message("Order updated", updated_order)

        # Insert log message
        await _insert_log_message(
            crud,
            order_id=updated_order["order_id"],
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
            order["resources"] = json.loads(order["resources"])
            order = utils_orders.format_order_display(order)

        return orders


async def _get_orders_query_params(statuses: list = [], record_id: str = "", user_id: str = "", order_id: str = ""):
    """
    SELECT complete order data by statuses, record_id, user_id and order_id
    Returns query and params
    """
    where_clauses = []
    params = {}

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

    query = """
    SELECT * FROM orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    """

    if where_clauses:
        query += "WHERE " + " AND ".join(where_clauses) + " "

    query += "ORDER BY o.order_id ASC"
    return query, params


async def _get_orders(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: str = "",
):
    query, params = await _get_orders_query_params(statuses, record_id, user_id, order_id)
    return await crud.query(query, params)


async def _get_orders_one(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: str = "",
):
    """
    Get orders by statuses, record_id, user_id and order_id
    """
    query, params = await _get_orders_query_params(statuses, record_id, user_id, order_id)
    order = await crud.query_one(query, params)
    return order


async def get_orders_admin(completed: int = 0):
    """
    Get all orders for a user. Allow to set status and finished.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        if completed:
            orders = await _get_orders(crud, [utils_orders.STATUSES_USER.COMPLETED])
        else:
            orders = await _get_orders(crud, [utils_orders.STATUSES_USER.ORDERED])

        for order in orders:
            order["resources"] = json.loads(order["resources"])
            order = utils_orders.format_order_display(order)
            queued_orders = await _get_orders(crud, [utils_orders.STATUSES_USER.QUEUED], order["record_id"])
            order["count"] = len(queued_orders)

        return orders


async def get_order(order_id):
    """
    Get a single joined order by order_id
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        order = await _get_orders_one(CRUD(connection), order_id=order_id)
        return order


async def _insert_log_message(crud: "CRUD", order_id, location, user_status, changed_by):
    log_message = {
        "order_id": order_id,
        "location": location,
        "user_status": user_status,
        "changed_by": changed_by,
    }

    await crud.insert("orders_log", log_message)
