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
    -- identifier TEXT NOT NULL,                        -- Barcode/box_id
    -- location TEXT,                                   -- Building-level location
    created TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- label TEXT,                                      -- Label for the order
    deadline TEXT,
    client_id TEXT,
    status_modified TEXT,
    status_updated_by TEXT,
    status TEXT CHECK(status IN (
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


# List of migrations with keys
migrations = {
    "create_orders": create_orders_query,
}


try:
    db_path = settings["sqlite3"]["orders"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations)
migration_manager.run_migrations()
migration_manager.close()
