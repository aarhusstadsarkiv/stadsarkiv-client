from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.database import utils_orders as utils
from stadsarkiv_client.core.logging import get_log
import json


log = get_log()

try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""

STATUSES_ORDER = utils.STATUSES_LOCATION


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def get_active_order(self, user_id: str, record_id: str, statuses=None, connection=None):
        query = f"""
        SELECT *
        FROM orders o
        LEFT JOIN records r ON o.record_id = r.record_id
        WHERE r.record_id = :record_id
        AND o.user_id = :user_id
        AND o.user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED});
        """
        order = await self.queryOne(query, {"user_id": user_id, "record_id": record_id}, connection=connection)
        return order

    async def is_record_active_by_user(self, user_id: str, record_id: str, connection=None):
        statuses = f"{utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED}"
        row = await self.get_active_order(user_id, record_id, connection=connection)
        return row is not None

    async def get_active_orders_by_record_id(self, record_id: str, connection):
        """
        Get all active orders connected to a record
        """
        query = f"""
        SELECT *
        FROM orders o
        LEFT JOIN records r ON o.record_id = r.record_id
        WHERE r.record_id = :record_id
        AND o.user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
        ORDER BY o.created_at ASC
        """
        orders = await self.query(query, {"record_id": record_id}, connection=connection)
        return orders

    async def count_active_users(self, record_id: str, connection=None):
        """
        Get count of active users on a record
        """
        rows = await self.get_active_orders_by_record_id(record_id, connection=connection)
        num_rows = len(rows)
        return num_rows

    async def is_owner_of_order(self, user_id: str, order_id: int):

        filters = {"order_id": order_id, "user_id": user_id}
        is_owner = await database_orders.exists(
            table="orders",
            filters=filters,
        )

        return is_owner

    async def insert_order(self, meta_data: dict, me: dict):

        # Check if user is already active on this record

        async with self.transaction_scope() as connection:

            """
            Check if there are other active users on this record that are orderable
            If so, set status to QUEUED, otherwise set status to ORDERED
            """

            # Check if user is already active on this record
            is_active_by_user = await self.is_record_active_by_user(me["id"], meta_data["id"], connection=connection)
            if is_active_by_user:
                # This may happen is user has already ordered the record
                # In reality it will only happen if the user has two tabs open and POST the same order twice
                raise Exception("User is already active on this record")

            # get user
            user_data = await self.select_one("users", filters={"user_id": me["id"]}, connection=connection)
            if not user_data:
                await self.insert("users", utils.get_insert_user_data(me), connection=connection)
                user_data = await self.select_one("users", filters={"user_id": me["id"]}, connection=connection)

            # get record
            record_data = await self.select_one("records", filters={"record_id": meta_data["id"]}, connection=connection)
            if not record_data:
                await self.insert("records", utils.get_insert_record_data(meta_data), connection=connection)
                record_data = await self.select_one("records", filters={"record_id": meta_data["id"]}, connection=connection)

            # Check if active order exists on record.
            # If so, set status to QUEUED, otherwise set status to ORDERED
            num_active_orders = await self.count_active_users(meta_data["id"], connection=connection)
            if num_active_orders > 0:
                user_status = utils.STATUSES_USER.QUEUED
            else:
                user_status = utils.STATUSES_USER.ORDERED

            await self.insert(
                "orders",
                utils.get_order_data(user_data["user_id"], record_data["record_id"], user_status),
                connection=connection,
            )

            last_order_id = await self.last_insert_id(connection=connection)
            order_data = await self.select_one("orders", filters={"order_id": last_order_id}, connection=connection)

            # Send message to user
            utils.send_order_message("Order created", order_data)

            # Insert log message
            await self.insert_log_message(
                order_id=order_data["order_id"],
                location=record_data["location"],
                user_status=order_data["user_status"],
                changed_by=me["id"],
                connection=connection,
            )

    async def insert_log_message(self, order_id, location, user_status, changed_by, connection):
        log_message = {
            "order_id": order_id,
            "location": location,
            "user_status": user_status,
            "changed_by": changed_by,
        }
        await self.insert("orders_log", log_message, connection=connection)

    async def get_orders_user(self, user_id: str, completed=0):
        """
        Get all orders for a user. Exclude orders with specific statuses.
        """
        async with self.transaction_scope() as connection:

            if completed:
                query = f"""
                SELECT * FROM orders o
                LEFT JOIN records r ON o.record_id = r.record_id
                WHERE o.user_id = :user_id
                AND o.user_status IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
                """
            else:
                query = f"""
                SELECT * FROM orders o
                LEFT JOIN records r ON o.record_id = r.record_id
                WHERE o.user_id = :user_id
                AND o.user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
                """

            filters = {"user_id": user_id}

            orders = await self.query(query, filters, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = utils.format_order_display(order)

            return orders

    async def update_admin_order(self, update_values: dict, filters: dict, user_id: str):
        """
        Update order. User has to own the order or be an employee
        """
        async with self.transaction_scope() as connection:

            await database_orders.update(
                table="orders",
                update_values={"deadline": update_values["deadline"], "comment": update_values["comment"]},
                filters=filters,
                connection=connection,
            )

            updated_order = await self.get_order(filters["order_id"], connection=connection)
            await database_orders.update(
                table="records",
                update_values={"location": updated_order["location"]},
                filters={"record_id": updated_order["record_id"]},
                connection=connection,
            )

            updated_record = await self.select_one("records", filters={"record_id": updated_order["record_id"]}, connection=connection)

            # TODO: If location AVAILABLE_IN_READING_ROOM. Send message to user

            # Send message to user
            utils.send_order_message("Order updated", updated_order)

            # Insert log message
            await self.insert_log_message(
                order_id=updated_order["order_id"],
                location=updated_record["location"],
                user_status=updated_order["user_status"],
                changed_by=user_id,
                connection=connection,
            )

        """
        In case of a order changing to completed we must check if another order is waiting for the same record.
        Select all orders with the same record_id and status ORDERED order by created_at ASC.
        If so, we must update the status of that order to AVAILABLE_IN_READING_ROOM and send a message to the user.
        """

    async def update_user_order(self, update_values: dict, filters: dict, user_id: str):
        """
        Update order. User has to own the order or be an employee
        """
        async with self.transaction_scope() as connection:

            await database_orders.update(
                table="orders",
                update_values=update_values,
                filters=filters,
                connection=connection,
            )

            updated_order = await self.get_order(filters["order_id"], connection=connection)

            # Send message to user
            utils.send_order_message("Order updated", updated_order)

            # Insert log message
            await self.insert_log_message(
                order_id=updated_order["order_id"],
                location=updated_order["location"],
                user_status=updated_order["user_status"],
                changed_by=user_id,
                connection=connection,
            )

    async def get_orders_admin(self, completed: int = 0):
        """
        Get all orders for a user. Allow to set status and finished.
        """
        async with self.transaction_scope() as connection:

            statuses_hidden = [utils.STATUSES_USER.COMPLETED, utils.STATUSES_USER.DELETED]
            completed_statuses_str = utils.get_sql_in_str(statuses_hidden)

            statuses_hidden_with_queued = [utils.STATUSES_USER.COMPLETED, utils.STATUSES_USER.DELETED, utils.STATUSES_USER.QUEUED]
            completed_statuses_str_with_queued = utils.get_sql_in_str(statuses_hidden_with_queued)

            if completed:
                query = f"""
                SELECT * FROM orders o
                LEFT JOIN records r ON o.record_id = r.record_id
                LEFT JOIN users u ON o.user_id = u.user_id
                WHERE o.user_status IN ({completed_statuses_str})
                """
            else:
                # in admin view do not show orders that are queued
                query = f"""
                SELECT * FROM orders o
                LEFT JOIN records r ON o.record_id = r.record_id
                LEFT JOIN users u ON o.user_id = u.user_id
                WHERE o.user_status NOT IN ({completed_statuses_str_with_queued})
                """

            query += " ORDER BY o.order_id ASC"

            orders = await self.query(query, {}, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = utils.format_order_display(order)
                order["count"] = await self.count_active_users(order["record_id"], connection=connection)

            return orders

    async def get_order(self, order_id, connection=None):

        query = """
        SELECT * FROM orders o
        LEFT JOIN records r ON o.record_id = r.record_id
        LEFT JOIN users u ON o.user_id = u.user_id
        WHERE o.order_id = :order_id
        """

        order = await database_orders.queryOne(query, {"order_id": order_id}, connection=connection)
        order = dict(order)
        order["resources"] = json.loads(order["resources"])
        order = utils.format_order_display(order)

        return order


database_orders = OrdersCRUD(orders_url)
