import sqlite3
import typing
from stadsarkiv_client.database.utils import transaction_scope
from stadsarkiv_client.core.logging import get_log


log = get_log()
DATABASE_ORDERS = "orders"


async def orders_insert(order_details: dict):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:

            columns = ", ".join(order_details.keys())
            placeholders = ", ".join([f":{key}" for key in order_details.keys()])

            query = f"INSERT INTO orders ({columns}) VALUES ({placeholders})"
            connection.execute(query, order_details)
        except sqlite3.Error as e:
            raise e


async def orders_get_by_user_id(user_id: str) -> typing.List[dict]:
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:
            query = "SELECT * FROM orders WHERE user_id = :user_id"
            result = connection.execute(query, {"user_id": user_id})
            return result.fetchall()
        except sqlite3.Error:
            raise


async def orders_update(order_id: int, update_values: dict):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:
            set_clause = ", ".join([f"{key} = :{key}" for key in update_values.keys()])
            query = f"UPDATE orders SET {set_clause} WHERE id = :order_id"

            update_values["order_id"] = order_id
            connection.execute(query, update_values)
        except sqlite3.Error:
            raise


async def orders_delete(order_id: int):
    async with transaction_scope(DATABASE_ORDERS) as connection:
        try:
            query = "DELETE FROM orders WHERE id = :order_id"
            connection.execute(query, {"order_id": order_id})
        except sqlite3.Error:
            raise


def get_info_from_record(record: dict):
    """
    http://localhost:5555/records/000503354
    identifikation: "51648293"

    http://localhost:5555/records/000504168
    storage_id: ['91+01390-2']

    000429798

    (None, '8038476141', 'Reol 106/fag 2/hylde 1')

    000506083

    (['91+01418-1'], None, None)

    """

    try:
        storage_id = record["resources"][0]["storage_id"]
    except KeyError:
        storage_id = None

    try:
        barcode = record["resources"][0]["barcode"]
    except KeyError:
        barcode = None

    try:
        location = record["resources"][0]["location"]
    except KeyError:
        location = None

    return storage_id, barcode, location
