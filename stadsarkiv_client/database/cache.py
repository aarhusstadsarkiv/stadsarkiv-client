"""
Simple sqlite3 cache implementation
Example usage:

```
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
        "result": result,
        "has_result": has_result,
        "expire": cache_expire,
        "inserted_value": insert_value,
    }
)
```
"""

from stadsarkiv_client.core.dynamic_settings import settings
import sqlite3
import json
import time
from typing import Any
from stadsarkiv_client.database.utils import DatabaseConnection

try:
    database_url = settings["sqlite3"]["default"]
except KeyError:
    database_url = ""

database_transation = DatabaseConnection(database_url)
transaction_scope = database_transation.transaction_scope_async


async def cache_set(key: str, data: Any) -> bool:
    """
    Set a cache value. This will always delete the old value and insert a new one.
    """
    json_data = json.dumps(data)

    async with transaction_scope() as connection:
        try:
            connection.execute("DELETE FROM cache WHERE key = ?", (key,))
            connection.execute("INSERT INTO cache (key, value, unix_timestamp) VALUES (?, ?, ?)", (key, json_data, int(time.time())))
            return True

        except sqlite3.Error:
            raise


async def cache_get(key: str, expire_in: int = 0) -> Any:
    """
    Will return the value if the key exists and is not expired.
    Will return None if the key does not exist or if the key is expired.
    If expire_in is 0, the value will never expire.
    """
    async with transaction_scope() as connection:
        try:
            result = connection.execute("SELECT * FROM cache WHERE key = ?", (key,)).fetchone()

            if result:
                if expire_in == 0:
                    return json.loads(result["value"])

                current_time = int(time.time())
                if current_time - result["unix_timestamp"] < expire_in:
                    return json.loads(result["value"])
                else:
                    connection.execute("DELETE FROM cache WHERE id = ?", (result["id"],))
            return None

        except sqlite3.Error:
            raise


async def cache_delete(id: int) -> None:
    """
    Delete a cache value by id
    """
    async with transaction_scope() as connection:
        try:
            connection.execute("DELETE FROM cache WHERE id = ?", (id,))

        except sqlite3.Error:
            raise
