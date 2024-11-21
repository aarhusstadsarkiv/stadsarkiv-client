from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.database.sql_builder import SQLBuilder
import sqlite3

log = get_log()

try:
    database_url = settings["sqlite3"]["orders"]
except KeyError:
    database_url = ""


class OrdersCRUD(CRUD):
    def __init__(self, database_url: str, table: str):
        super().__init__(database_url, table)

    async def order_patch_user(self, update_values: dict, filters: dict):
        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder("orders")
                query = sql_builder.build_update(update_values=update_values, filters=filters)
                connection.execute(query, sql_builder.values)

            except sqlite3.Error as e:
                raise e


crud_orders = OrdersCRUD(database_url=database_url, table="orders")
