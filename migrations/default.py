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
import sys

sys.path.append(".")

from maya.core.dynamic_settings import settings
from maya.core.migration import Migration
from maya.migrations.default import migrations_default
from maya.core.logging import get_log
import os

# Check if the environment variable CONFIG_DIR is set
if "BASE_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export BASE_DIR=example-config-aarhus")
    exit(1)


log = get_log()


try:
    db_path = settings["sqlite3"]["default"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations_default)
migration_manager.run_migrations()
migration_manager.close()
