import sqlite3
from stadsarkiv_client.database.utils import transaction_scope
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder

log = get_log()


class CRUD:
    def __init__(self, database: str, table: str):
        self.database = database
        self.table = table
        self.sql_builder = SQLBuilder(self.table)

    async def insert(self, data: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_insert(data)
                connection.execute(query, data)
            except sqlite3.Error as e:
                raise e

    async def insert_many(self, data: list):
        async with transaction_scope(self.database) as connection:
            try:
                for single_data in data:
                    query = self.sql_builder.build_insert(single_data)
                    connection.execute(query, single_data)
            except sqlite3.Error as e:
                raise e

    async def select(self, filters: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_select(filters)
                result = connection.execute(query, filters)
                rows = result.fetchall()
                return rows
            except sqlite3.Error as e:
                raise e

    async def exists(self, filters: dict):
        rows = await self.select(filters)
        return bool(rows)

    async def update(self, update_values: dict, filters: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_update(update_values, filters)
                connection.execute(query, update_values)
            except sqlite3.Error as e:
                raise e

    async def delete(self, filters: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_delete(filters)
                log.debug(f"query: {query}")
                connection.execute(query, filters)
            except sqlite3.Error as e:
                raise e
