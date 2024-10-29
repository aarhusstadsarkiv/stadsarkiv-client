#!/usr/bin/env python
"""
# Set a config dir as environment variable and run this script to create the database tables.
export CONFIG_DIR=example-config-aarhus
./bin/create_db_tables.py
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.core.logging import get_log


log = get_log()


create_booksmarks_query = """
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    bookmark TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;
"""

create_booksmarks_index_query = """
CREATE INDEX idx_bookmarks_user_id ON bookmarks (user_id);
"""

create_searches_query = """
CREATE TABLE searches (
    id INTEGER PRIMARY KEY,
    search TEXT NOT NULL,
    title TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
) STRICT;
"""

create_searches_index_query = """
CREATE INDEX idx_searches_user_id ON searches (user_id);
"""

create_cache_query = """
CREATE TABLE cache (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    value TEXT,
    unix_timestamp INTEGER DEFAULT 0
) STRICT;
"""

create_cache_index_query = """
CREATE INDEX idx_cache_key ON cache (key);
"""

create_error_logs = """
CREATE TABLE error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    error TEXT,
    error_code INTEGER,
    exception TEXT,
    resolved BOOLEAN DEFAULT 0,
    UNIQUE(url, error)
)
"""

# List of migrations with keys
migrations = {
    "create_bookmarks": create_booksmarks_query,
    "create_bookmarks_index": create_booksmarks_index_query,
    "create_searches": create_searches_query,
    "create_searches_index": create_searches_index_query,
    "create_cache": create_cache_query,
    "create_cache_index": create_cache_index_query,
    "create_error_logs": create_error_logs,
}


try:
    db_path = settings["sqlite3"]["default"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations)
migration_manager.run_migrations()
migration_manager.close()
