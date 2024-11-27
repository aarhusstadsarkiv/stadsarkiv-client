from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
import typing


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


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def is_ordered(self, user_id: str, record_id: str):
        """
        Check if a user has ordered this record. This is the case
        if the user does not have a order with:
        """
        filters = {"user_id": user_id, "record_id": record_id, "finished": 0}
        return await self.select_one(table="orders", filters=filters)

    async def is_owner(self, user_id: str, order_id: str):

        filters = {"order_id": order_id, "user_id": user_id}
        is_owner = await database_orders.exists(
            table="orders",
            filters=filters,
        )

        return is_owner

    async def insert_order(self, meta_data: dict, me: dict):
        """
        Insert a new order and associate the user who initiated it.
        """
        order_data = _get_order_insert_data(meta_data, me)
        await self.insert("orders", order_data)

    async def get_orders_by_user(self, user_id: str, finished: int = 0):
        """
        Get all orders for a user. Get finished orders if finished is set to 1.
        """
        filters = {"user_id": user_id, "finished": finished}
        return await self.select(table="orders", filters=filters)

    async def update_order(self, update_values: dict, filters: dict):

        await database_orders.update(
            table="orders",
            update_values=update_values,
            filters=filters,
        )


database_orders = OrdersCRUD(orders_url)
