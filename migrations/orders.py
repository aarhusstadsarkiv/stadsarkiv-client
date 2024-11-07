#!/usr/bin/env python
"""

Adds option for uses ordering materials from the archive to create the database tables.

export CONFIG_DIR=example-config-aarhus
./bin/orders.py

"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.core.logging import get_log

log = get_log()

create_orders_query = """
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    -- identifier TEXT NOT NULL,                     -- "resources[].barcode" eller "resources[].storage_id[]
    barcode TEXT,                                    -- "resources[].barcode"
    storage_id TEXT,                                 -- "resources[].storage_id"
    location TEXT,                                   -- "resources[].location"
    created TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    label TEXT NOT NULL,                             -- Label for the order
    deadline TEXT,
    status_modified TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status_updated_by TEXT,
    status TEXT DEFAULT 'Ordered' CHECK(status IN (
        'Ordered',
        'Packed for reading room',
        'Available in the reading room',
        'Reading room',
        'Completed in the reading room',
        'To be returned to storage',
        'Completed'
    )),
    comment TEXT
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
