"""
A collection of functions for performing CRUD operations on orders.
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.database import utils_orders
from stadsarkiv_client.database.utils import DatabaseConnection
from stadsarkiv_client.core.logging import get_log


log = get_log()

try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""


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

        # Retrieve the newly created order
        last_order_id = await crud.last_insert_id()
        order_data = await _get_orders_one(crud, order_id=last_order_id)

        # Insert a log entry for the new order
        await _insert_log_message(
            crud,
            order_id=order_data["order_id"],
            location=record_data["location"],
            user_status=order_data["user_status"],
            updated_by=me["id"],
        )

        # Handle special cases for orders already in the reading room and ordered
        if record_data["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM and user_status == utils_orders.STATUSES_USER.ORDERED:
            log.debug(f"Order {order_data['order_id']} moved to READING_ROOM. Setting deadline and sending message.")

            deadline_date = utils_orders.get_deadline_date()
            order_data["deadline"] = deadline_date

            # Update order with deadline and message status
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date, "message_sent": 1},
                filters={"order_id": order_data["order_id"]},
            )

            updated_order = await _get_orders_one(crud, order_id=order_data["order_id"])
            utils_orders.send_order_message("Order available in reading room", updated_order)

        return order_data


async def _update_user_status(crud: "CRUD", order_id: int, new_status: int):
    """
    Updates the user status of an order. If the order's status is COMPLETED or DELETED, it checks for QUEUED orders
    on the same record. If found, updates the first QUEUED order to ORDERED and processes further actions.
    """
    order = await _get_orders_one(crud, order_id=order_id)
    if new_status in [utils_orders.STATUSES_USER.COMPLETED, utils_orders.STATUSES_USER.DELETED]:
        log.debug(f"Order {order_id}: Status changed to COMPLETED or DELETED.")

        next_queued_order = await _get_orders_one(crud, statuses=[utils_orders.STATUSES_USER.QUEUED], record_id=order["record_id"])
        if next_queued_order:
            log.debug(f"Order {next_queued_order['order_id']} found. Updating from QUEUED to ORDERED.")

            await crud.update(
                table="orders",
                update_values={"user_status": utils_orders.STATUSES_USER.ORDERED},
                filters={"order_id": next_queued_order["order_id"]},
            )

            if next_queued_order["location"] == utils_orders.STATUSES_LOCATION.READING_ROOM:
                log.debug(f"Order {next_queued_order['order_id']} moved to READING_ROOM.")

                deadline_date = utils_orders.get_deadline_date()
                await crud.update(
                    table="orders",
                    update_values={"deadline": deadline_date, "message_sent": 1},
                    filters={"order_id": next_queued_order["order_id"]},
                )

                next_queued_order = await _get_orders_one(crud, order_id=next_queued_order["order_id"])
                utils_orders.send_order_message("Order available in reading room", next_queued_order)


async def _update_location(crud: "CRUD", order_id: int, new_location: int):
    """
    Updates the location of a record. If the location changes to READING_ROOM, sets the deadline and sends a message.
    """
    if not new_location:
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
        log.debug(f"Order {order_id}: Location changed from {order['location']} to {new_location}.")

        # Log type of new_location and user_status

        if new_location == utils_orders.STATUSES_LOCATION.READING_ROOM:
            deadline_date = utils_orders.get_deadline_date()
            await crud.update(
                table="orders",
                update_values={"deadline": deadline_date, "message_sent": 1},
                filters={"order_id": order_id},
            )

            if not order.get("message_sent"):
                updated_order = await _get_orders_one(crud, order_id=order_id)
                utils_orders.send_order_message("Order available in reading room", updated_order)


async def update_order(location: int, update_values: dict, order_id: int, user_id: str):
    """
    Updates an order's details such as user status, deadline, and comment. Also handles location updates.
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
        await _update_location(crud, order_id, location)
        updated_order = await _get_orders_one(crud, order_id=order_id)
        await _update_user_status(crud, order_id, updated_order["user_status"])

        # Log the update
        await _insert_log_message(
            crud,
            order_id=order_id,
            location=updated_order["location"],
            user_status=updated_order["user_status"],
            updated_by=user_id,
        )


async def delete_order(order_id: int, user_id: str):
    """
    Delete an order by setting the user status to DELETED.
    """
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        # Update user status to DELETED
        await _update_user_status(crud, order_id, utils_orders.STATUSES_USER.DELETED)

        # Log the update
        await _insert_log_message(crud, order_id, 0, utils_orders.STATUSES_USER.DELETED, user_id)


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


async def get_orders_admin(
    filter_status: str,
    filter_location: str,
    filter_email: str,
    filter_user: str,
) -> list:
    """
    Get all orders for a user.
    """

    search_values = []
    search_filters = []
    if filter_location:
        search_filters.append("r.location =:location_filter")
        search_values.append(filter_location)
    if filter_email:
        search_filters.append("u.user_email LIKE :email_filter")
        search_values.append(filter_email)
    if filter_user:
        search_filters.append("u.user_display_name LIKE :user_filter")
        search_values.append(filter_user)

    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        search_filters_as_str = ""
        if search_filters:
            # add search filters to query
            search_filters_as_str = " AND " + " AND ".join(search_filters)
            log.debug(search_filters_as_str)

        if filter_status == "active":
            query = f"""
SELECT * FROM orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    WHERE o.user_status IN ({utils_orders.STATUSES_USER.ORDERED}) {search_filters_as_str} ORDER BY o.order_id DESC LIMIT 100
"""
            placeholder_values = {}
            if search_filters:
                placeholder_values = {
                    "location_filter": filter_location,
                    "email_filter": f"{filter_email}%",
                    "user_filter": f"{filter_user}%",
                }

            orders = await crud.query(query, placeholder_values)
            # log.debug(orders)
            # orders = await _get_orders(crud, statuses=[utils_orders.STATUSES_USER.ORDERED], order_by="o.order_id DESC")
            for order in orders:
                order = utils_orders.format_order_display(order)
                queued_orders = await _get_orders(crud, statuses=[utils_orders.STATUSES_USER.QUEUED], record_id=order["record_id"])
                order["count"] = len(queued_orders)

                # Only the first order in the list is 'ORDERED' and can be changed
                # if location is READING_ROOM set action_location_change to False
                if order["location"] != utils_orders.STATUSES_LOCATION.READING_ROOM:
                    order["allow_location_change"] = True

        if filter_status == "completed":
            query = f"""
WITH LatestOrders AS (
    SELECT
        o.record_id,
        MAX(o.updated_at) AS latest_updated_at
    FROM
        orders o
    GROUP BY
        o.record_id
)
SELECT
    o.*, r.*, u.*
FROM
    orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    INNER JOIN LatestOrders lo
        ON o.record_id = lo.record_id AND o.updated_at = lo.latest_updated_at
WHERE
    o.user_status IN ({utils_orders.STATUSES_USER.DELETED}, {utils_orders.STATUSES_USER.COMPLETED})
    AND
    r.location != {utils_orders.STATUSES_LOCATION.IN_STORAGE}

ORDER BY
    o.updated_at ASC
LIMIT 100;
"""
            orders = await crud.query(query, {})

            for order in orders:
                order = utils_orders.format_order_display(order)
                order["user_actions_deactivated"] = True
                order["allow_location_change"] = True

        if filter_status == "order_history":
            query = f"""
SELECT * FROM orders o
    LEFT JOIN records r ON o.record_id = r.record_id
    LEFT JOIN users u ON o.user_id = u.user_id
    WHERE o.user_status IN ({utils_orders.STATUSES_USER.DELETED}, {utils_orders.STATUSES_USER.COMPLETED})
    ORDER BY o.updated_at DESC LIMIT 100
"""
            # Get all orders with status COMPLETED
            # orders = await _get_orders(crud, statuses=[utils_orders.STATUSES_USER.COMPLETED], limit=100)
            orders = await crud.query(query, {})       
            for order in orders:
                order = utils_orders.format_order_display(order)
                order["user_actions_deactivated"] = True
                order["allow_location_change"] = False

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
        return order


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
    database_connection = DatabaseConnection(orders_url)
    async with database_connection.transaction_scope_async() as connection:
        crud = CRUD(connection)

        query = f"""
        SELECT * FROM orders
        WHERE deadline IS NOT NULL
        AND deadline < :current_date
        AND user_status = {utils_orders.STATUSES_USER.ORDERED}"""

        params = {"current_date": utils_orders.get_current_date_time()}

        orders = await crud.query(query, params)
        for order in orders:
            await _update_user_status(crud, order["order_id"], utils_orders.STATUSES_USER.COMPLETED)


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

    log.debug(query)
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


async def _insert_log_message(crud: "CRUD", order_id, location, user_status, updated_by):
    log_message = {
        "order_id": order_id,
        "location": location,
        "user_status": user_status,
        "updated_by": updated_by,
    }

    await crud.insert("orders_log", log_message)
