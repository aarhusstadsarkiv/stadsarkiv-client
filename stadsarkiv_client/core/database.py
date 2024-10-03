from stadsarkiv_client.core.logging import get_log
import sqlite3
import os
import typing
import json
import time
from typing import Any


DATABASE_URL = str(os.getenv("DATABASE_URL"))


log = get_log()


async def _get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


async def bookmarks_insert(user_id, bookmark) -> bool:

    connection = await _get_db_connection()
    cursor = connection.cursor()

    try:
        values = {"user_id": user_id, "bookmark": bookmark}
        query = "INSERT INTO bookmarks (user_id, bookmark) VALUES (:user_id, :bookmark)"
        cursor.execute(query, values)
        connection.commit()
        return True

    except sqlite3.Error as e:
        log.error(f"Failed to insert note: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


async def bookmarks_get(user_id) -> typing.Any:

    connection = await _get_db_connection()
    cursor = connection.cursor()

    try:
        values = {"user_id": user_id}
        query = "SELECT * FROM bookmarks WHERE user_id = :user_id"
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result

    except sqlite3.Error as e:
        log.error(f"Failed to get notes: {e}")
    finally:
        cursor.close()
        connection.close()


async def bookmarks_delete(user_id, bookmark_id) -> typing.Any:

    connection = await _get_db_connection()
    cursor = connection.cursor()

    try:
        values = {"bookmark": bookmark_id, "user_id": user_id}
        query = "DELETE FROM bookmarks WHERE bookmark = :bookmark AND user_id = :user_id"
        cursor.execute(query, values)
        connection.commit()

    except sqlite3.Error as e:
        log.error(f"Failed to delete note: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

"""

# Simple sqlite3 cache implementation
# Example usage:

```py
insert_value = None
# Get a result that is max 10 seconds old
cache_expire = 10
has_result = False

result = await database.cache_get("test", cache_expire)

if not result:
    # Set a new cache value
    insert_value = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
    await database.cache_set("test", {"random": insert_value})
else:
    has_result = True

return JSONResponse(
    {
        "message": "Test note inserted",
        "result": result,
        "has_result": has_result,
        "expire": cache_expire,
        "inserted_value": insert_value,
    }
)
```

"""


async def cache_set(key: str, data: Any):
    """
    Set a cache value
    """
    json_data = json.dumps(data)

    connection = await _get_db_connection()
    try:
        connection.execute("DELETE FROM cache WHERE key = ?", (key,))
        connection.execute("INSERT INTO cache (key, value, unix_timestamp) VALUES (?, ?, ?)", (key, json_data, int(time.time())))
        connection.commit()
        return True

    except sqlite3.Error as e:
        log.error(f"Failed to delete note: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()


async def cache_get(key: str, expire_in: int = 0) -> Any:
    """
    Will return the value if the key exists and is not expired
    Will return None if the key does not exist or if the key is expired
    """
    connection = await _get_db_connection()
    try:
        result = connection.execute("SELECT * FROM cache WHERE key = ?", (key,)).fetchone()

        if result:
            if expire_in == 0:
                return json.loads(result["value"])

            current_time = int(time.time())
            if current_time - result["unix_timestamp"] < expire_in:
                return json.loads(result["value"])
            else:
                await cache_delete(result["id"])
        return None
    finally:
        connection.close()


async def cache_delete(id: int):
    connection = await _get_db_connection()
    try:
        connection.execute("DELETE FROM cache WHERE id = ?", (id,))
        connection.commit()
    finally:
        connection.close()
