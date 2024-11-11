import sqlite3
from stadsarkiv_client.database.utils import transaction_scope
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder


log = get_log()
DATABASE_ORDERS = "orders"


async def orders_insert(order_details: dict):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:

            sql_builder = SQLBuilder("orders")
            query = sql_builder.build_insert(order_details)
            connection.execute(query, order_details)
        except sqlite3.Error as e:
            raise e


async def orders_select(filters: dict):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:

            sql_builder = SQLBuilder("orders")
            query = sql_builder.build_select(filters)

            result = connection.execute(query, filters)
            rows = result.fetchall()

            return rows
        except sqlite3.Error as e:
            raise e


async def orders_exists(filters: dict):
    rows = await orders_select(filters)
    if not rows:
        return False
    return True


async def orders_update(order_id: int, update_values: dict):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:
            sql_builder = SQLBuilder("orders")
            query = sql_builder.build_update(update_values, {"id": order_id})
            connection.execute(query, update_values)
        except sqlite3.Error:
            raise


async def orders_delete(order_id: int):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:
            sql_builder = SQLBuilder("orders")
            query = sql_builder.build_delete({"id": order_id})
            connection.execute(query, {"order_id": order_id})
        except sqlite3.Error:
            raise
