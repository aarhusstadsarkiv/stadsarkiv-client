#!/usr/bin/env python
"""
# Set a config dir as environment variable and run this script to create the database tables.
export CONFIG_DIR=example-config-aarhus
./bin/create_db_tables.py
"""

from stadsarkiv_client.core.dynamic_settings import init_settings
import sqlite3
from stadsarkiv_client.core.logging import get_log
import os

log = get_log()
init_settings()

DATABASE_URL = os.getenv("DATABASE_URL")
try:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
except ValueError:
    log.error("DATABASE_URL is not set in ENV")
    exit(1)


conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()


def check_migrations_table_exists():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations';")
    result = cursor.fetchone()
    return result is not None


def create_migrations_table_if_not_exists():
    if not check_migrations_table_exists():
        create_migrations_table = """
        CREATE TABLE migrations (
            id INTEGER PRIMARY KEY,
            migration_key VARCHAR(128),
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_migrations_table)
        conn.commit()
        log.info("Migrations table created.")
    else:
        log.info("Migrations table already exists.")


create_migrations_table_if_not_exists()


create_booksmarks_query = """
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    bookmark VARCHAR(128),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_booksmarks_index_query = """
CREATE INDEX idx_bookmarks_user_id ON bookmarks (user_id);
"""

create_searches_query = """
CREATE TABLE searches (
    id INTEGER PRIMARY KEY,
    search VARCHAR(1024),
    title VARCHAR(256),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_searches_index_query = """
CREATE INDEX idx_searches_user_id ON searches (user_id);
"""

create_cache_query = """
CREATE TABLE cache (
    id INTEGER PRIMARY KEY,
    key VARCHAR(128),
    value TEXT,
    unix_timestamp INTEGER DEFAULT 0
);
"""

create_cache_index_query = """
CREATE INDEX idx_cache_key ON cache (key);
"""

# List of migrations with keys
migrations = {
    "create_bookmarks": create_booksmarks_query,
    "create_bookmarks_index": create_booksmarks_index_query,
    "create_searches": create_searches_query,
    "create_searches_index": create_searches_index_query,
    "create_cache": create_cache_query,
    "create_cache_index": create_cache_index_query,
}


def has_migration_been_applied(migration_key):
    cursor.execute("SELECT 1 FROM migrations WHERE migration_key = ?", (migration_key,))
    return cursor.fetchone() is not None


def apply_migration(migration_key, sql):
    if not has_migration_been_applied(migration_key):
        cursor.execute(sql)
        conn.commit()
        log.info(f"SQL for {migration_key} executed")
        cursor.execute("INSERT INTO migrations (migration_key) VALUES (?)", (migration_key,))
        conn.commit()
        log.info(f"Migration {migration_key} recorded")


def create_tables():
    for migration_key, sql in migrations.items():
        apply_migration(migration_key, sql)


create_tables()
conn.close()
