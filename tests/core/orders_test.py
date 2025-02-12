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
        Simple integration test for orders
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

        log.info("Assert no orders")
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertFalse(has_active_order)

        log.info("Insert order")
        await crud_orders.insert_order(meta_data, record_and_types, me)

        with self.assertRaises(Exception) as cm:  # Capture the exception
            log.info("Insert order again and assert raises")
            await crud_orders.insert_order(meta_data, record_and_types, me)

        log.info("Asset correct exception message")
        self.assertIn("User is already active on this record", str(cm.exception))

        log.info("Assert user has active order")
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertTrue(has_active_order)

        log.info("Assert no deadline on order")
        order = await crud_orders.get_order("1")
        self.assertIsNone(order["deadline"])

        log.info("Assert 1 order and no completed orders or order history") 
        orders_filter = crud_orders.OrderFilter()
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        orders_filter = crud_orders.OrderFilter(filter_status="completed")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        orders_filter = crud_orders.OrderFilter(filter_status="order_history")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        log.info("Assert 1 log message (insert order)")
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 1)

        



if __name__ == "__main__":
    unittest.main()
