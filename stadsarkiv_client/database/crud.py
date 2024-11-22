"""
Small CRUD class to handle basic database operations using sqlite3.

```
from stadsarkiv_client.database.crud import CRUD

database_url = settings["sqlite3"]["default"]
crud_example = CRUD(database_url=database_url)

async def example():
    await crud_example.insert("orders", {"order_id": 1, "order_name": "order1"})
    await crud_example.insert("orders", {"order_id": 2, "order_name": "order2"})

    many_orders = [
        {"order_id": 3, "order_name": "test"},
        {"order_id": 4, "order_name": "test"},
    ]
    await crud_example.insert_many("orders", many_orders)

    await crud_example.select(
        "orders",
        columns=["order_id"],
        filters={"order_name": "test"},
        order_by=[("order_id", "ASC")],
        limit_offset=(2, 0),
    )

    await curd_example.select_one("orders", columns=["order_id"], filters={"order_name": "test"})

    await crud_example.exists("orders", {"order_name": "test"})
    await crud_example.update("orders", {"order_name": "new test"}, {"order_id": 3})
    await crud_example.delete("orders", {"order_id": 4})

class OrdersCRUD(CRUD):
    def __init__(self, database_url: str):
        super().__init__(database_url)

    async def new_method(self):

        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_update(update_values=update_values, filters=filters)
                connection.execute(query, sql_builder.get_execute_values())

            except sqlite3.Error as e:
                raise e

```
"""

import sqlite3
from stadsarkiv_client.database.utils import DatabaseTransaction
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder

log = get_log()


class CRUD:
    def __init__(self, database_url: str):
        """
        Initialize CRUD with database URL table name.
        """
        database_transation = DatabaseTransaction(database_url)
        self.transaction_scope = database_transation.transaction_scope

    def set_table(self, table: str):
        """
        Change the current table you are working with.
        """
        self.table = table

    async def insert(self, table: str, insert_values: dict):
        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_insert(insert_values)
                connection.execute(query, insert_values)
            except sqlite3.Error as e:
                raise e

    async def insert_many(self, table: str, insert_values_many: list):
        async with self.transaction_scope() as connection:
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
    ) -> list:
        async with self.transaction_scope() as connection:
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

    async def select_one(self, table: str, columns: list = [], filters: dict = {}) -> dict:
        rows = await self.select(table=table, columns=columns, filters=filters, limit_offset=(1, 0))
        if rows:
            return dict(rows[0])
        return {}

    async def update(self, table, update_values: dict, filters: dict):
        """
        Update rows by update_values and filters
        """
        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_update(update_values, filters)
                connection.execute(query, sql_builder.get_execute_values())
            except sqlite3.Error as e:
                raise e

    async def delete(self, table: str, filters: dict):
        """
        Delete rows by filters
        """
        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_delete(filters)
                connection.execute(query, filters)
            except sqlite3.Error as e:
                raise e

    async def exists(self, table, filters: dict):
        rows = await self.select_one(table=table, filters=filters)
        return bool(rows)

    async def count(self, table: str, filters: dict, column: str = "*") -> int:
        async with self.transaction_scope() as connection:
            try:
                sql_builder = SQLBuilder(table)
                query = sql_builder.build_select(columns=[f"COUNT({column}) as num_rows"], filters=filters)
                result = connection.execute(query, filters)
                row = result.fetchone()
                return row["num_rows"]
            except sqlite3.Error as e:
                raise e
