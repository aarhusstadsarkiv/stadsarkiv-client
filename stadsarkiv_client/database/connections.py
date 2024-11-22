from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder
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

    async def order_patch_user(self, table: str, update_values: dict, filters: dict):

        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_update(update_values=update_values, filters=filters)
                connection.execute(query, sql_builder.values)

            except sqlite3.Error as e:
                raise e


database_default = CRUD(database_url=default_url)
database_orders = OrdersCRUD(database_url=orders_url)
