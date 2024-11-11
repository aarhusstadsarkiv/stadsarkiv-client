class SQLBuilder:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def build_insert(self, data: dict) -> str:
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{key}" for key in data.keys()])
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

    def build_select(self, filters: dict = {}) -> str:
        query = f"SELECT * FROM {self.table_name}"
        if filters:
            where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
            query += f" WHERE {where_clause}"
        return query

    def build_update(self, update_values: dict, filters: dict) -> str:
        set_clause = ", ".join([f"{key} = :{key}" for key in update_values.keys()])
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"

    def build_delete(self, filters: dict) -> str:
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
        return f"DELETE FROM {self.table_name} WHERE {where_clause}"
