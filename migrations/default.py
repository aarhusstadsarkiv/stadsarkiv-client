#!/usr/bin/env python
"""

The system will work fine without database tables, but some features will not be available.

- Bookmarks
- Searches
- Cache
- Import logs
- Error logs in DB format

Install:

Set a config dir as environment variable and run this script to create the database tables.

E.g.:

export CONFIG_DIR=example-config-aarhus
./bin/default.py
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.core.logging import get_log
import os

# Check if the environment variable CONFIG_DIR is set
if "CONFIG_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export CONFIG_DIR=example-config-aarhus")
    exit(1)


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
    time TEXT,
    name TEXT,
    level TEXT,
    message TEXT,
    exception TEXT,
    url TEXT,
    error_code INTEGER,
    resolved INTEGER DEFAULT 0,
    UNIQUE(url, message)
) STRICT;
"""

create_error_logs_index = """
CREATE INDEX idx_time ON error_logs (time);
"""

# alter bookmarks table bookmark column name to record_id
alter_bookmarks_table = """
ALTER TABLE bookmarks RENAME COLUMN bookmark TO record_id;
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
    "create_error_logs_index": create_error_logs_index,
    "alter_bookmarks_table": alter_bookmarks_table,
}


try:
    db_path = settings["sqlite3"]["default"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations)
migration_manager.run_migrations()
migration_manager.close()
