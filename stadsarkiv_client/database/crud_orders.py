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

STATUSES_ORDER = utils.STATUSES_ADMIN


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def insert_log_message(self, order_data, user_id, connection):
        log_message = {
            "order_id": order_data["order_id"],
            "location": order_data["location"],
            "user_status": order_data["user_status"],
            "changed_by": user_id,
        }
        await self.insert("orders_log", log_message, connection=connection)

    async def is_record_active_by_user(self, user_id: str, record_id: str, connection=None):
        query = f"""
        SELECT * FROM orders
        WHERE user_id = :user_id
        AND record_id = :record_id
        AND user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
        """

        rows = await self.query(query, {"user_id": user_id, "record_id": record_id}, connection=connection)
        return len(rows) > 0

    async def is_active_by_any_user(self, record_id: str, connection=None):
        rows = await self.get_orders_by_record_id(record_id, connection=connection)
        return len(rows)

    async def get_orders_by_record_id(self, record_id: str, connection):
        query = f"""
        SELECT * FROM orders
        WHERE record_id = :record_id
        AND user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
        ORDER BY created_at ASC
        """

        order = await self.query(query, {"record_id": record_id}, connection=connection)
        return order

    async def is_owner_of_order(self, user_id: str, order_id: int):

        filters = {"order_id": order_id, "user_id": user_id}
        is_owner = await database_orders.exists(
            table="orders",
            filters=filters,
        )

        return is_owner

    async def insert_order(self, meta_data: dict, me: dict):

        # Check if user is already active on this record
        is_active_by_user = await self.is_record_active_by_user(me["id"], meta_data["id"])
        if is_active_by_user:
            raise Exception("User is already active on this record")

        async with self.transaction_scope() as connection:

            """
            Check if there are other active users on this record
            If so, set status to QUEUED, otherwise set status to ORDERED
            If status is QUEUED, set location to the location of the first active order
            (all orders have the same location)
            If status is ORDERED, location is None
            """

            num_active_users = await self.is_active_by_any_user(meta_data["id"], connection=connection)
            if num_active_users:
                user_status = utils.STATUSES_USER.QUEUED
                rows = await self.get_orders_by_record_id(meta_data["id"], connection=connection)
                location = rows[0]["location"]
            else:
                user_status = utils.STATUSES_USER.ORDERED
                location = utils.STATUSES_ADMIN.WAITING

            order_data = utils.get_order_insert_data(meta_data, me, location, user_status)
            await self.insert("orders", order_data, connection=connection)
            last_order_id = await self.last_insert_id(connection=connection)

            # Get the inserted order, send message, and insert log message
            inserted_order = await self.select_one("orders", filters={"order_id": last_order_id}, connection=connection)
            utils.send_order_message("Order created", inserted_order)
            await self.insert_log_message(inserted_order, order_data["user_id"], connection=connection)

    async def get_orders_user(self, user_id: str, completed=0):
        """
        Get all orders for a user. Exclude orders with specific statuses.
        """
        async with self.transaction_scope() as connection:

            if completed:
                query = f"""
                SELECT * FROM orders
                WHERE user_id = :user_id
                AND user_status IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
                """
            else:
                query = f"""
                SELECT * FROM orders
                WHERE user_id = :user_id
                AND user_status NOT IN ({utils.STATUSES_USER.COMPLETED}, {utils.STATUSES_USER.DELETED})
                """

            filters = {"user_id": user_id}

            orders = await self.query(query, filters, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = utils.format_order_display(order)

            return orders

    async def update_order(self, update_values: dict, filters: dict, user_id: str):
        async with self.transaction_scope() as connection:

            await database_orders.update(
                table="orders",
                update_values=update_values,
                filters=filters,
                connection=connection,
            )

            # Get the updated order, send message, and insert log message
            updated_order = await self.select_one("orders", filters=filters, connection=connection)
            utils.send_order_message("Order updated", updated_order)
            await self.insert_log_message(updated_order, user_id, connection=connection)
        """
        In case of a order changing to completed we must check if another order is waiting for the same record.
        Select all orders with the same record_id and status ORDERED order by created_at ASC.
        If so, we must update the status of that order to AVAILABLE_IN_READING_ROOM and send a message to the user.
        """

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
                SELECT * FROM orders
                WHERE user_status IN ({completed_statuses_str})
                """
            else:
                # in admin view do not show orders that are queued
                query = f"""
                SELECT * FROM orders
                WHERE user_status NOT IN ({completed_statuses_str_with_queued})
                """

            query += " ORDER BY order_id ASC"

            orders = await self.query(query, {}, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = utils.format_order_display(order)

            return orders

    async def get_order(self, order_id):
        order = await database_orders.select_one(table="orders", filters={"order_id": order_id})
        order["resources"] = json.loads(order["resources"])
        order = utils.format_order_display(order)

        return order


database_orders = OrdersCRUD(orders_url)
