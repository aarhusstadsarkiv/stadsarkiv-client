import asyncio
from stadsarkiv_client.core.dynamic_settings import init_settings
from stadsarkiv_client.core.logging import get_log
import unittest
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.migrations.orders import migrations_orders
from stadsarkiv_client.database import crud, utils
import os
from stadsarkiv_client.database import crud_orders
from stadsarkiv_client.database import utils_orders
import json

init_settings()
log = get_log()


class TestDB(unittest.TestCase):

    def test_insert_order(self):
        asyncio.run(self._test_insert_order_async())

    async def _test_insert_order_async(self):
        """
        Integration test for insert_order function
        """
        db_path = "/tmp/orders.db"
        if os.path.exists(db_path):
            os.remove(db_path)

        migration = Migration(db_path=db_path, migrations=migrations_orders)
        migration.run_migrations()

        me_data_file = "tests/data/me.json"
        with open(me_data_file) as f:
            me = json.load(f)

        meta_data_file = "tests/data/meta_data_000495102.json"
        with open(meta_data_file) as f:
            meta_data = json.load(f)

        record_and_types_file = "tests/data/record_and_types_000495102.json"
        with open(record_and_types_file) as f:
            record_and_types = json.load(f)

        # Insert order
        await crud_orders.insert_order(meta_data, record_and_types, me)
        print("Order inserted")

        # Insert again and exception exception("User is already active on this record")
        with self.assertRaises(Exception) as _:
            print("Order already inserted")
            await crud_orders.insert_order(meta_data, record_and_types, me)


if __name__ == "__main__":
    unittest.main()
