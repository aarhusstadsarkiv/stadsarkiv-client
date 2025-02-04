"""
A collection of functions for performing CRUD operations on orders.
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.database import utils_orders
from stadsarkiv_client.database.utils import DatabaseConnection
from stadsarkiv_client.core.logging import get_log
from dataclasses import dataclass
from typing import Optional


log = get_log()


try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""


MAIL_SENT = "Mail sendt"
LOCATION_CHANGED = "Lokation ændret"
ORDER_CREATED = "Bestilling oprettet"
ORDER_COMPLETED = "Bestilling afsluttet"
STATUS_CHANGED = "Bruger status ændret"


@dataclass
class OrderFilter:
    # Filter options
    filter_status: str = "active"
    filter_location: Optional[str] = ""
    filter_email: Optional[str] = ""
    filter_user: Optional[str] = ""
    filter_show_queued: Optional[str] = ""
    filter_limit: int = 50
    filter_offset: int = 0

    # Pagination
    filter_has_next: bool = False
    filter_has_prev: bool = False
    filter_next_offset: int = 0
    filter_prev_offset: int = 0


async def has_active_order(user_id: str, record_id: str):
    """
    Check if user has an active order on a record
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        return await _has_active_order(crud, user_id, record_id)


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


async def replace_employee(me: dict):
    """
    Insert or update employee details
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)
        user_data = utils_orders.get_insert_user_data(me)
        await crud.replace("users", user_data, {"user_id": me["id"]})


async def _has_active_order(crud: "CRUD", user_id: str, record_id: str):
    """
    Check if user has an active order on a record
    """
    statuses = [utils_orders.STATUSES_USER.ORDERED, utils_orders.STATUSES_USER.QUEUED]
    order = await _get_orders_one(crud, statuses, record_id, user_id)
    return order


async def insert_order(meta_data: dict, record_and_types: dict, me: dict):
    """
    Insert an order into the database with proper validations and updates.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        # Check for active order by the user on the same record
        if await _has_active_order(crud, me["id"], meta_data["id"]):
            raise Exception("User is already active on this record")

        # Insert or update user details
        user_data = utils_orders.get_insert_user_data(me)
        await crud.replace("users", user_data, {"user_id": me["id"]})

        # Fetch or prepare record data
        record_db = await crud.select_one("records", filters={"record_id": meta_data["id"]})
        if record_db:
            record_data = utils_orders.get_insert_record_data(meta_data, record_and_types, record_db["location"])
        else:
            record_data = utils_orders.get_insert_record_data(meta_data, record_and_types)

        await crud.replace("records", record_data, {"record_id": meta_data["id"]})

        # Determine user status based on active orders for the record
        active_order = await _get_orders_one(crud, [utils_orders.STATUSES_USER.ORDERED], meta_data["id"])
        user_status = utils_orders.STATUSES_USER.QUEUED if active_order else utils_orders.STATUSES_USER.ORDERED

        # Create new order data
        order_data = utils_orders.get_order_data(
            user_data["user_id"],
            record_data["record_id"],
            user_status,
        )

        await crud.insert("orders", order_data)

        # Retrieve the newly created order and log the creation
        last_order_id = await crud.last_insert_id()
        inserted_order = await _get_orders_one(crud, order_id=last_order_id)
        log_messages = [ORDER_CREATED]

        # Handle special cases for orders already in the reading room and ordered
        if record_data["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM and user_status == utils_orders.STATUSES_USER.ORDERED:

            deadline_date = utils_orders.get_deadline_date()
            inserted_order["deadline"] = deadline_date

            # Update order with deadline and message status
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date, "message_sent": 1},
                filters={"order_id": inserted_order["order_id"]},
            )

            updated_order = await _get_orders_one(crud, order_id=inserted_order["order_id"])
            await utils_orders.send_order_message("Order available in reading room", updated_order)
            log_messages.append(MAIL_SENT)

        await _insert_log_message(
            crud,
            user_id=inserted_order["user_id"],
            order=inserted_order,
            message=". ".join(log_messages),
        )

        return inserted_order


async def _update_user_status(crud: "CRUD", user_id: str, order_id: int, new_status: int):
    """
    Updates the user status of an order. If the order's status is COMPLETED or DELETED, it checks for QUEUED orders
    on the same record. If found, updates the first QUEUED order to ORDERED and processes further actions.
    """
    order = await _get_orders_one(crud, order_id=order_id)
    if new_status in [utils_orders.STATUSES_USER.COMPLETED, utils_orders.STATUSES_USER.DELETED]:
        await _insert_log_message(
            crud,
            user_id,
            order,
            STATUS_CHANGED,
        )

        next_queued_order = await _get_orders_one(crud, statuses=[utils_orders.STATUSES_USER.QUEUED], record_id=order["record_id"])
        if next_queued_order:
            # Update the status of the next queued order to ORDERED
            await crud.update(
                table="orders",
                update_values={"user_status": utils_orders.STATUSES_USER.ORDERED},
                filters={"order_id": next_queued_order["order_id"]},
            )
            log_messages = [STATUS_CHANGED]

            if next_queued_order["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM:
                # Update the deadline and send a message if the order is in the reading room
                log.debug(f"Order {next_queued_order['order_id']} moved to READING_ROOM.")

                deadline_date = utils_orders.get_deadline_date()
                await crud.update(
                    table="orders",
                    update_values={"deadline": deadline_date, "message_sent": 1},
                    filters={"order_id": next_queued_order["order_id"]},
                )

                next_queued_order = await _get_orders_one(crud, order_id=next_queued_order["order_id"])
                await utils_orders.send_order_message("Order available in reading room", next_queued_order)
                log_messages.append(MAIL_SENT)

            # Log the status change
            await _insert_log_message(
                crud,
                user_id=user_id,
                order=next_queued_order,
                message=". ".join(log_messages),
            )


async def _update_location(crud: "CRUD", user_id: str, order_id: int, new_location: int):
    """
    Updates the location of a record. If the location changes to READING_ROOM, sets the deadline and sends a message.
    """
    if not new_location:
        log.debug("No location provided for update")
        return

    order = await _get_orders_one(crud, order_id=order_id)
    record_id = order["record_id"]

    await _allow_location_change(crud, record_id, raise_exception=True)
    await crud.update(
        table="records",
        update_values={"location": new_location},
        filters={"record_id": record_id},
    )

    if order["location"] != new_location:
        log.debug(f"Record {record_id} moved from {order['location']} to {new_location}")
        log_messages = [LOCATION_CHANGED]

        # Update order location
        order["location"] = new_location

        if new_location == utils_orders.STATUSES_LOCATION.READING_ROOM:
            log.debug(f"Order {order_id} moved to READING_ROOM.")

            deadline_date = utils_orders.get_deadline_date()
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date, "message_sent": 1},
                filters={"order_id": order_id},
            )

            if not order.get("message_sent"):
                updated_order = await _get_orders_one(crud, order_id=order_id)
                await utils_orders.send_order_message("Order available in reading room", updated_order)
                log_messages.append(MAIL_SENT)

        await _insert_log_message(
            crud,
            user_id=user_id,
            order=order,
            message=". ".join(log_messages),
        )
    else:
        log.debug("Order not moved to READING_ROOM.")


async def update_order(
    order_id: int,
    user_id: str,
    location: int,
    update_values: dict,
):
    """
    Updates an order's details such as user status (deadline, and comment). Also handles location updates.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        # Update order details
        update_values["updated_at"] = utils_orders.get_current_date_time()
        await crud.update(
            table="orders",
            update_values=update_values,
            filters={"order_id": order_id},
        )

        # Handle location or user status updates
        await _update_location(crud, user_id, order_id, location)
        updated_order = await _get_orders_one(crud, order_id=order_id)
        await _update_user_status(crud, user_id, order_id, updated_order["user_status"])


async def _get_queued_orders_length(crud: "CRUD", orders: list[dict]) -> dict:
    """
    From a list of order get the count of queued orders for each record in the list
    """
    records_ids = [order["record_id"] for order in orders]
    list_of_record_ids = ", ".join([f"'{record_id}'" for record_id in records_ids])

    # query for getting count of queued orders for any record in the list
    query = f"""
SELECT record_id, COUNT(*) AS queued_count
FROM orders
WHERE user_status IN ({utils_orders.STATUSES_USER.QUEUED})
AND record_id IN ({list_of_record_ids})
GROUP BY record_id
ORDER BY queued_count DESC;
"""
    queued_orders = await crud.query(query, {})
    queued_orders_dict = {order["record_id"]: order["queued_count"] for order in queued_orders}

    return queued_orders_dict


async def get_orders_user(user_id: str, completed=0) -> list:
    """
    Get all orders for a user. Exclude orders with specific statuses.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        # Define the statuses based on the `completed` flag
        statuses = (
            [utils_orders.STATUSES_USER.COMPLETED] if completed else [utils_orders.STATUSES_USER.ORDERED, utils_orders.STATUSES_USER.QUEUED]
        )

        # Fetch the orders based on statuses
        orders = await _get_orders(crud, statuses=statuses, user_id=user_id)

        # Format each order for display
        return [format_order_for_display(order) for order in orders]


def _get_and_filters_str_and_values(filters: OrderFilter) -> tuple:
    search_values = []
    search_filters = []
    if filters.filter_location:
        search_filters.append("r.location =:location_filter")
        search_values.append(filters.filter_location)
    if filters.filter_email:
        search_filters.append("u.user_email LIKE :email_filter")
        search_values.append(filters.filter_email)
    if filters.filter_user:
        search_filters.append("u.user_display_name LIKE :user_filter")
        search_values.append(filters.filter_user)

    placeholder_values = {}
    if search_filters:
        placeholder_values = {
            "location_filter": filters.filter_location,
            "email_filter": f"{filters.filter_email}%",
            "user_filter": f"{filters.filter_user}%",
        }

    search_filters_as_str = ""
    if search_filters:
        search_filters_as_str = " AND " + " AND ".join(search_filters)

    return search_filters_as_str, placeholder_values


async def _get_active_orders(crud: "CRUD", filters: OrderFilter, offset: int = 0) -> list:
    search_filters_as_str, placeholder_values = _get_and_filters_str_and_values(filters)

    if filters.filter_show_queued:
        user_statuses = f"{utils_orders.STATUSES_USER.ORDERED}, {utils_orders.STATUSES_USER.QUEUED}"
    else:
        user_statuses = f"{utils_orders.STATUSES_USER.ORDERED}"

    query = f"""
SELECT o.*, r.*, u.*
FROM orders o
LEFT JOIN records r ON o.record_id = r.record_id
LEFT JOIN users u ON o.user_id = u.user_id
WHERE o.user_status IN ({user_statuses})
{search_filters_as_str}
ORDER BY o.order_id DESC
LIMIT {filters.filter_limit} OFFSET {offset}
"""

    orders = await crud.query(query, placeholder_values)
    return orders


async def _get_completed_orders(crud: "CRUD", filters: OrderFilter, offset: int = 0) -> list:
    search_filters_as_str, placeholder_values = _get_and_filters_str_and_values(filters)
    query = f"""
SELECT o.*, r.*, u.*
FROM orders o
LEFT JOIN records r ON o.record_id = r.record_id
LEFT JOIN users u ON o.user_id = u.user_id
WHERE
    -- Only COMPLETED orders
    o.user_status IN ({utils_orders.STATUSES_USER.COMPLETED}, {utils_orders.STATUSES_USER.DELETED})

    -- Make sure we pick the most recent COMPLETED order for each record
    AND o.updated_at = (
        SELECT MAX(o2.updated_at)
        FROM orders o2
        WHERE o2.record_id = o.record_id
          AND o2.user_status IN ({utils_orders.STATUSES_USER.COMPLETED}, {utils_orders.STATUSES_USER.DELETED})
    )

    -- Exclude records that have an ORDERED status
    AND o.record_id NOT IN (
        SELECT record_id
        FROM orders
        WHERE user_status = {utils_orders.STATUSES_USER.ORDERED}
    )

    -- Also exclude records with location = IN_STORAGE
    -- AND r.location <> {utils_orders.STATUSES_LOCATION.IN_STORAGE}

    -- Search filters
    {search_filters_as_str}

    ORDER BY o.updated_at DESC
    LIMIT {filters.filter_limit} OFFSET {offset}

"""
    # log.debug(f"query: {query}")
    orders = await crud.query(query, placeholder_values)
    return orders


async def _get_history_orders(crud: "CRUD", filters: OrderFilter, offset: int = 0) -> list:
    search_filters_as_str, placeholder_values = _get_and_filters_str_and_values(filters)

    query = f"""
SELECT o.*, r.*, u.*
    FROM orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    WHERE o.user_status IN ({utils_orders.STATUSES_USER.DELETED}, {utils_orders.STATUSES_USER.COMPLETED})
    {search_filters_as_str}
    ORDER BY o.updated_at DESC
    LIMIT {filters.filter_limit} OFFSET {offset}
"""
    orders = await crud.query(query, placeholder_values)
    return orders


async def get_orders_admin(filters: OrderFilter) -> tuple[list, OrderFilter]:
    """
    Get all orders for a user.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        offset = filters.filter_offset
        if filters.filter_status == "active":
            orders = await _get_active_orders(crud, filters, offset)
            queued_orders = await _get_queued_orders_length(crud, orders)

            for order in orders:
                order = utils_orders.format_order_display(order)

                record_id = order["record_id"]
                order["count"] = queued_orders.get(record_id, 0)

                # Only the first order in the list is 'ORDERED' and can be changed
                # if location is READING_ROOM set action_location_change to False
                if order["location"] != utils_orders.STATUSES_LOCATION.READING_ROOM:
                    order["allow_location_change"] = True

            offset_next = offset + filters.filter_limit
            orders_next = await _get_active_orders(crud, filters, offset_next)

        if filters.filter_status == "completed":
            orders = await _get_completed_orders(crud, filters, offset)

            for order in orders:
                order = utils_orders.format_order_display(order)
                order["user_actions_deactivated"] = True
                order["allow_location_change"] = True

            offset_next = offset + filters.filter_limit
            orders_next = await _get_completed_orders(crud, filters, offset_next)

        if filters.filter_status == "order_history":
            orders = await _get_history_orders(crud, filters, offset)

            for order in orders:
                order = utils_orders.format_order_display(order)
                order["user_actions_deactivated"] = True
                order["allow_location_change"] = False

            offset_next = offset + filters.filter_limit
            orders_next = await _get_history_orders(crud, filters, offset_next)

        # Generate pagination
        # log.debug(f"num orders next {len(orders_next)}")
        has_next = bool(len(orders_next))
        if has_next:
            next_offset = filters.filter_offset + filters.filter_limit
        else:
            next_offset = 0

        has_prev = bool(filters.filter_offset > 0)
        if has_prev:
            prev_offset = filters.filter_offset - filters.filter_limit
        else:
            prev_offset = 0

        filters.filter_has_next = has_next
        filters.filter_has_prev = has_prev
        filters.filter_next_offset = next_offset
        filters.filter_prev_offset = prev_offset

        return orders, filters


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
        return order


async def get_logs(order_id: str = "") -> list:
    """
    Get a single joined order by order_id for display on the admin edit order page
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        sql = []
        values = {}
        if order_id:
            sql.append("l.order_id = :order_id")
            values = {"order_id": order_id}

        where_sql = ""
        if sql:
            where_sql = "WHERE " + " AND ".join(sql)
        query = f"""
SELECT * FROM orders_log l
JOIN orders o ON l.order_id = o.order_id
JOIN users u ON l.user_id = u.user_id
JOIN records r ON l.record_id = r.record_id
{where_sql}
ORDER BY l.updated_at DESC
LIMIT 100
"""

        logs = await crud.query(query, values)
        for single_log in logs:
            single_log = utils_orders.format_log_display(single_log)
        return logs


async def get_order_by_record_id(user_id: str, record_id: str):
    """
    Get a single order by record_id
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        order = await _get_orders_one(CRUD(connection), user_id=user_id, record_id=record_id)
        return order


def format_order_for_display(order: dict):
    """
    Format order for display
    """
    order = utils_orders.format_order_display(order)
    return order


async def cron_orders():
    """
    Deadline may look like this: 2024-12-25 09:23:52
    Check if deadline has passed and update user status to COMPLETED
    """
    if not settings.get("cron_orders", False):
        log.debug("Cron orders is disabled")
        return

    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        query = f"""
        SELECT * FROM orders
        WHERE deadline IS NOT NULL
        AND deadline < :current_date
        AND user_status = {utils_orders.STATUSES_USER.ORDERED}"""

        params = {"current_date": utils_orders.get_current_date_time()}

        user_id = "SYSTEM"
        orders = await crud.query(query, params)
        for order in orders:

            full_order = await _get_orders_one(crud, order_id=order["order_id"])
            await crud.update(
                table="orders",
                update_values={"user_status": utils_orders.STATUSES_USER.COMPLETED},
                filters={"order_id": full_order["order_id"]},
            )

            await _update_user_status(crud, user_id, full_order["order_id"], utils_orders.STATUSES_USER.COMPLETED)
            # await _insert_log_message(
            #     crud,
            #     user_id,
            #     full_order,
            #     ORDER_COMPLETED,
            # )


async def _get_orders(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: int = 0,
    location: int = 0,
    order_by: str = "o.order_id DESC",
    limit: int = 100,
):
    query, params = await _get_orders_query_params(
        statuses,
        record_id,
        user_id,
        order_id,
        location,
        order_by,
        limit,
    )

    result = await crud.query(query, params)
    return result


async def _get_orders_one(
    crud: "CRUD",
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: int = 0,
    location: int = 0,
    order_by: str = "o.order_id DESC",
    limit: int = 1,
):
    """
    Get a single order
    """
    query, params = await _get_orders_query_params(
        statuses,
        record_id,
        user_id,
        order_id,
        location,
        order_by,
        limit,
    )
    order = await crud.query_one(query, params)
    return order


async def _get_orders_query_params(
    statuses: list = [],
    record_id: str = "",
    user_id: str = "",
    order_id: int = 0,
    location: int = 0,
    order_by: str = "o.order_id DESC",
    limit: int = 0,
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

    if order_by:
        query += f"ORDER BY {order_by} "

    if limit:
        query += f"LIMIT {limit} "

    return query, params


async def _allow_location_change(crud: "CRUD", record_id: str, raise_exception=False):
    """
    Check if location can be changed
    Get orders where location is READING_ROOM and user_status is ORDERED
    If there are no orders then location can be changed
    """
    orders = await _get_orders(
        crud,
        statuses=[utils_orders.STATUSES_USER.ORDERED],
        location=utils_orders.STATUSES_LOCATION.READING_ROOM,
        record_id=record_id,
    )
    if orders:
        if raise_exception:
            raise Exception(f"Lokation kan ikke ændres. Der er allerede en bestilling med record_id {record_id} i læsesalen")
        return False
    return True


async def _insert_log_message(
    crud: "CRUD",
    user_id: str,
    order: dict,
    message: str,
):
    log_message = {
        "user_id": user_id,
        "order_id": order["order_id"],
        "record_id": order["record_id"],
        "updated_location": order["location"],
        "updated_user_status": order["user_status"],
        "message": message,
    }

    """
    order_id=order_id,
    record_id=updated_order["record_id"],
    location=updated_order["location"],
    user_status=updated_order["user_status"],
    """

    await crud.insert("orders_log", log_message)
