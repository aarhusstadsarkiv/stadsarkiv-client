import sqlite3
import logging

log = logging.getLogger(__name__)


MIGRATION_TABLE_SQL = """
CREATE TABLE migrations (
    id INTEGER PRIMARY KEY,
    migration_key TEXT NOT NULL,
    applied_at TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;
"""


class Migration:
    def __init__(self, db_path, migrations):

        self.migrations = migrations
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_migrations_table_if_not_exists()

    def _check_migrations_table_exists(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations';")
        result = self.cursor.fetchone()
        return result is not None

    def _create_migrations_table_if_not_exists(self):
        if not self._check_migrations_table_exists():
            self.cursor.execute(MIGRATION_TABLE_SQL)
            self.conn.commit()
            log.info("Migrations table created.")
        else:
            log.info("Migrations table already exists.")

    def _has_migration_been_applied(self, migration_key):
        self.cursor.execute("SELECT 1 FROM migrations WHERE migration_key = ?", (migration_key,))
        return self.cursor.fetchone() is not None

    def _apply_migration(self, migration_key, sql):
        if not self._has_migration_been_applied(migration_key):
            self.cursor.execute(sql)
            self.conn.commit()
            log.info(f"SQL for {migration_key} executed")
            self.cursor.execute("INSERT INTO migrations (migration_key) VALUES (?)", (migration_key,))
            self.conn.commit()
            log.info(f"Migration {migration_key} recorded")

    def run_migrations(self):
        for migration_key, sql in self.migrations.items():
            self._apply_migration(migration_key, sql)

    def close(self):
        self.conn.close()
