import sqlite3
import typing
from stadsarkiv_client.core.database.utils import transaction_scope


async def bookmarks_insert(user_id, bookmark):

    async with transaction_scope() as connection:
        try:
            values = {"user_id": user_id, "bookmark": bookmark}
            query = "INSERT INTO bookmarks (user_id, bookmark) VALUES (:user_id, :bookmark)"
            connection.execute(query, values)

        except sqlite3.Error:
            raise


async def bookmarks_get(user_id) -> typing.Any:
    async with transaction_scope() as connection:
        try:
            values = {"user_id": user_id}
            query = "SELECT * FROM bookmarks WHERE user_id = :user_id"
            cursor = connection.execute(query, values)
            result = cursor.fetchall()
            return result

        except sqlite3.Error:
            raise


async def bookmarks_delete(user_id, bookmark_id) -> typing.Any:
    async with transaction_scope() as connection:
        try:
            values = {"bookmark": bookmark_id, "user_id": user_id}
            query = "DELETE FROM bookmarks WHERE bookmark = :bookmark AND user_id = :user_id"
            connection.execute(query, values)

        except sqlite3.Error:
            raise
