from stadsarkiv_client.core.dynamic_settings import settings
import sqlite3
from contextlib import asynccontextmanager, contextmanager
from stadsarkiv_client.core.logging import get_log


log = get_log()


def get_db_connection_sync(database_url: str) -> sqlite3.Connection:
    connection = sqlite3.connect(database_url)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


@contextmanager
def transaction_scope_sync(database: str = "default"):
    database_url = settings["sqlite3"][database]
    connection = get_db_connection_sync(database_url)
    try:
        connection.execute("BEGIN IMMEDIATE")
        yield connection
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


async def get_db_connection(database_url: str) -> sqlite3.Connection:
    """
    https://kerkour.com/sqlite-for-servers
    """
    connection = sqlite3.connect(database_url)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


@asynccontextmanager
async def transaction_scope(database: str = "default"):
    """
    Use transaction_scope to create a transaction.

    Usage example:
    See stadsarkiv_client/core/database/cache.py
    """
    database_url = settings["sqlite3"][database]
    connection = await get_db_connection(database_url)
    try:

        connection.execute("BEGIN IMMEDIATE")
        yield connection

        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()
