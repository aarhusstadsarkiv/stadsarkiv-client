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
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL UNIQUE,
    user_display_name TEXT NOT NULL
) STRICT;

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    user_status INTEGER NOT NULL,
    record_id TEXT NOT NULL,
    deadline TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    comment TEXT DEFAULT "",
    message_sent INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (record_id) REFERENCES records(record_id)
) STRICT;

CREATE TABLE records (
    record_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    resources TEXT,
    location INTEGER NOT NULL
) STRICT;

CREATE TABLE orders_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    user_status INTEGER,
    location INTEGER,
    changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
) STRICT;

-- Indexes for foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_record_id ON orders(record_id);
CREATE INDEX idx_orders_log_order_id ON orders_log(order_id);

-- Indexes other
CREATE INDEX idx_users_user_email ON users(user_email);
CREATE INDEX idx_orders_user_status ON orders(user_status);
CREATE INDEX idx_orders_deadline ON orders(deadline);
CREATE INDEX idx_records_location ON records(location);
CREATE INDEX idx_orders_log_changed_at ON orders_log(changed_at);
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
