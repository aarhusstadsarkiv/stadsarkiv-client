#!/usr/bin/env python
"""

Adds option for uses ordering materials from the archive to create the database tables.

export CONFIG_DIR=example-config-aarhus
./bin/orders.py

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

create_orders_query = """
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    user_display_name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    label TEXT NOT NULL,                             -- Label for the order
    deadline TEXT,
    modified_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_by TEXT,
    resources TEXT,                                  -- JSON array of resources
    status TEXT DEFAULT 'ORDERED' CHECK(status IN (
        'ORDERED',
        'PACKED_FOR_READING_ROOM',
        'AVAILABLE_IN_READING_ROOM',
        'COMPLETED_IN_READING_ROOM',
        'RETURN_TO_STORAGE',
        'COMPLETED'
    )),
    comment TEXT,
    done INTEGER DEFAULT 0 CHECK(done IN (0, 1))
) STRICT;
"""

create_user_index_query = """
CREATE INDEX idx_orders_user_id ON orders (user_id);
"""

create_status_index_query = """
CREATE INDEX idx_orders_status ON orders (status);
"""

# List of migrations with keys
migrations = {
    "create_orders": create_orders_query,
    "create_user_index": create_user_index_query,
    "create_status_index": create_status_index_query,
}

try:
    db_path = settings["sqlite3"]["orders"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations)
migration_manager.run_migrations()
migration_manager.close()
