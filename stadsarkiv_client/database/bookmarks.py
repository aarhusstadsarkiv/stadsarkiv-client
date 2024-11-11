import sqlite3
import typing
from stadsarkiv_client.database.utils import transaction_scope
from stadsarkiv_client.database.sql_builder import SQLBuilder


async def bookmarks_insert(values: dict):

    async with transaction_scope() as connection:
        try:
            sql_builder = SQLBuilder("bookmarks")
            query = sql_builder.build_insert(values)
            connection.execute(query, values)

        except sqlite3.Error:
            raise


async def bookmarks_insert_many(user_id: str, bookmarks: list):

    async with transaction_scope() as connection:
        try:
            for bookmark in bookmarks:
                values = {"user_id": user_id, "bookmark": bookmark}
                sql_builder = SQLBuilder("bookmarks")
                query = sql_builder.build_insert(values)
                connection.execute(query, values)

        except sqlite3.Error:
            raise


async def bookmarks_get(values: dict) -> typing.Any:
    async with transaction_scope() as connection:
        try:

            sql_builder = SQLBuilder("bookmarks")
            query = sql_builder.build_select(values)

            cursor = connection.execute(query, values)
            result = cursor.fetchall()
            return result

        except sqlite3.Error:
            raise


async def bookmarks_delete(values: dict) -> typing.Any:
    async with transaction_scope() as connection:
        try:
            sql_builder = SQLBuilder("bookmarks")
            query = sql_builder.build_delete(values)
            connection.execute(query, values)

        except sqlite3.Error:
            raise
