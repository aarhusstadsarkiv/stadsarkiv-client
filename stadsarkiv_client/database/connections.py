from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log
import sqlite3

log = get_log()

try:
    default_url = settings["sqlite3"]["default"]
except KeyError:
    default_url = ""

try:
    orders_url = settings["sqlite3"]["orders"]
except KeyError:
    orders_url = ""


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def order_patch_by_admin(self, record_id: str):

        async with self.transaction_scope() as connection:
            try:

                # Only get orders that are not done
                query = "SELECT id FROM orders WHERE record_id = :record_id and done = 0"
                cursor = connection.execute(query, {"record_id": record_id, "done": 0})
                rows = cursor.fetchall()
                rows = [dict(row) for row in rows]
                log.debug(f"result: {rows}")

            except sqlite3.Error as e:
                raise e


database_default = CRUD(default_url)
database_orders = OrdersCRUD(orders_url)
