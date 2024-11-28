from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from dataclasses import asdict
import typing
from stadsarkiv_client.core import date_format


log = get_log()

try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""


@dataclasses.dataclass
class OrderStatuses:
    """
    Possible statuses for an order
    """

    ORDERED: int = 1
    PACKED_FOR_READING_ROOM: int = 2
    AVAILABLE_IN_READING_ROOM: int = 3
    COMPLETED_IN_READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5
    COMPLETED: int = 6


STATUSES_ORDER = OrderStatuses()
STATUSES_ORDER_DICT = asdict(STATUSES_ORDER)

STATUSES_HUMAN = {
    1: "Bestilt",
    2: "Pakket til læsesalen",
    3: "Tilgængelig i læsesalen",
    4: "Afsluttet i læsesalen",
    5: "Retur til magasin",
    6: "Afsluttet",
}


def _get_order_insert_data(meta_data: dict, me: dict):
    """
    Generate data for inserting into orders table
    """
    order_inser_data = {
        # record data
        "record_id": meta_data["id"],
        "label": meta_data["title"],
        "resources": json.dumps(meta_data["resources"]),
        # user data
        "user_id": me["id"],
        "user_email": me["email"],
        "user_display_name": me["display_name"],
        # status
        "status": STATUSES_ORDER.ORDERED,
    }
    return order_inser_data


def format_order_display(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    order["created_at"] = date_format.timezone_alter(order["created_at"])
    order["updated_at"] = date_format.timezone_alter(order["updated_at"])
    if order["deadline"]:
        order["deadline"] = date_format.timezone_alter(order["deadline"])

    order["status_human"] = STATUSES_HUMAN.get(order["status"])
    return order


def send_order_message(message: str, order: dict):
    log.debug(f"Sending {message} about order: {order}")


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def insert_log_message(self, order_data, user_id, connection):
        """
        Insert a log message for an order.
        """
        log_message = {
            "order_id": order_data["order_id"],
            "status": order_data["status"],
            "changed_by": user_id,
        }
        await self.insert("orders_log", log_message, connection=connection)

    async def is_ordered(self, user_id: str, record_id: str):
        """
        Check if a user has ordered this record. That means he has a order with a status other than completed.
        """

        query = f"""
        SELECT * FROM orders
        WHERE user_id = :user_id
        AND record_id = :record_id
        AND status NOT IN ({STATUSES_ORDER.COMPLETED})
        """

        rows = await self.query(query, {"user_id": user_id, "record_id": record_id})
        return len(rows) > 0

    async def is_owner(self, user_id: str, order_id: int):

        filters = {"order_id": order_id, "user_id": user_id}
        is_owner = await database_orders.exists(
            table="orders",
            filters=filters,
        )

        return is_owner

    async def insert_order(self, meta_data: dict, me: dict):
        """
        Insert a new order.
        """
        async with self.transaction_scope() as connection:
            order_data = _get_order_insert_data(meta_data, me)
            await self.insert("orders", order_data, connection=connection)
            last_order_id = await self.last_insert_id(connection=connection)

            # Get the inserted order, send message, and insert log message 
            inserted_order = await self.select_one('orders', filters={"order_id": last_order_id}, connection=connection)
            send_order_message("Order created", inserted_order)
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
                AND status = {STATUSES_ORDER.COMPLETED})
                """
            else:
                query = f"""
                SELECT * FROM orders
                WHERE user_id = :user_id
                AND status NOT IN ({STATUSES_ORDER.COMPLETED})
                """

            filters = {"user_id": user_id}

            orders = await self.query(query, filters, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = format_order_display(order)

            return orders

    async def update_order(self, update_values: dict, filters: dict, user_id: str):
        """
        Update an order with new values.
        """
        async with self.transaction_scope() as connection:
            await database_orders.update(
                table="orders",
                update_values=update_values,
                filters=filters,
                connection=connection,
            )

            # Get the updated order, send message, and insert log message
            updated_order = await self.select_one('orders', filters=filters, connection=connection)
            send_order_message("Order created", updated_order)
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

            if completed:
                query = f"""
                SELECT * FROM orders
                WHERE status = {STATUSES_ORDER.COMPLETED})
                """
            else:
                query = f"""
                SELECT * FROM orders
                WHERE status NOT IN ({STATUSES_ORDER.COMPLETED})
                """

            query += " ORDER BY order_id ASC"

            orders = await self.query(query, {}, connection=connection)
            for order in orders:
                order["resources"] = json.loads(order["resources"])
                order = format_order_display(order)

            return orders

    async def get_order(self, order_id):
        order = await database_orders.select_one(table="orders", filters={"order_id": order_id})
        order["resources"] = json.loads(order["resources"])
        order = format_order_display(order)

        return order


database_orders = OrdersCRUD(orders_url)
