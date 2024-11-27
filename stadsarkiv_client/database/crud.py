import sqlite3
from stadsarkiv_client.database.utils import DatabaseConnection
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder

log = get_log()


class CRUD:
    def __init__(self, database_url: str):
        """
        Initialize CRUD with database URL.
        """
        database_connection = DatabaseConnection(database_url)
        self.transaction_scope = database_connection.transaction_scope_async

    async def last_insert_id(self, connection) -> int:
        """
        Get the last inserted row ID.
        """
        try:
            cursor = connection.execute("SELECT last_insert_rowid() as last_insert_id")
            row = cursor.fetchone()
            return row["last_insert_id"]
        except sqlite3.Error as e:
            raise e

    async def insert(self, table: str, insert_values: dict, connection=None):
        """
        Insert a single row into the table.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                await self.insert(table, insert_values, connection=connection)
                return
        try:
            sql_builder = SQLBuilder(table)
            query = sql_builder.build_insert(insert_values)
            connection.execute(query, insert_values)
        except sqlite3.Error as e:
            raise e

    async def insert_many(self, table: str, insert_values_many: list, connection=None):
        """
        Insert multiple rows into the table.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                await self.insert_many(table, insert_values_many, connection=connection)
                return
        try:
            for single_data in insert_values_many:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_insert(single_data)
                connection.execute(query, single_data)
        except sqlite3.Error as e:
            raise e

    async def select(
        self,
        table: str,
        columns: list = [],
        filters: dict = {},
        order_by: list = [],
        limit_offset: tuple = (),
        connection=None,
    ) -> list:
        """
        Select rows from the table.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                return await self.select(table, columns, filters, order_by, limit_offset, connection=connection)
        try:
            sql_builder = SQLBuilder(table)
            query = sql_builder.build_select(
                columns=columns,
                filters=filters,
                order_by=order_by,
                limit_offset=limit_offset,
            )
            result = connection.execute(query, filters)
            rows = result.fetchall()
            rows = [dict(row) for row in rows]
            return rows
        except sqlite3.Error as e:
            raise e

    async def select_one(self, table: str, columns: list = [], filters: dict = {}, connection=None) -> dict:
        """
        Select a single row from the table.
        """
        rows = await self.select(table=table, columns=columns, filters=filters, limit_offset=(1, 0), connection=connection)
        if rows:
            return dict(rows[0])
        return {}

    async def update(self, table: str, update_values: dict, filters: dict, connection=None):
        """
        Update rows in the table.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                await self.update(table, update_values, filters, connection=connection)
                return
        try:
            sql_builder = SQLBuilder(table)
            query = sql_builder.build_update(update_values, filters)
            connection.execute(query, sql_builder.get_execute_values())
        except sqlite3.Error as e:
            raise e

    async def delete(self, table: str, filters: dict, connection=None):
        """
        Delete rows from the table.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                await self.delete(table, filters, connection=connection)
                return
        try:
            sql_builder = SQLBuilder(table)
            query = sql_builder.build_delete(filters)
            connection.execute(query, filters)
        except sqlite3.Error as e:
            raise e

    async def exists(self, table: str, filters: dict, connection=None) -> bool:
        """
        Check if any row exists matching the filters.
        """
        row = await self.select_one(table=table, filters=filters, connection=connection)
        return bool(row)

    async def count(self, table: str, filters: dict, column: str = "*", connection=None) -> int:
        """
        Count rows in the table matching the filters.
        """
        if connection is None:
            async with self.transaction_scope() as connection:
                return await self.count(table, filters, column, connection=connection)
        try:
            sql_builder = SQLBuilder(table)
            query = sql_builder.build_select(columns=[f"COUNT({column}) as num_rows"], filters=filters)
            result = connection.execute(query, filters)
            row = result.fetchone()
            return row["num_rows"]
        except sqlite3.Error as e:
            raise e
