import asyncio
from stadsarkiv_client.core.dynamic_settings import init_settings
from stadsarkiv_client.core.logging import get_log
import unittest
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.migrations.orders import migrations_orders
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

        me_2 = me.copy()
        me_2["id"] = "ANOTHER_USER_ID"
        me_2["email"] = "another.email@example.com"

        log.info("Assert no orders")
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertFalse(has_active_order)

        log.info("Insert order")
        await crud_orders.insert_order(meta_data, record_and_types, me)

        with self.assertRaises(Exception) as cm:  # Capture the exception
            log.info("Insert order again and assert raises")
            await crud_orders.insert_order(meta_data, record_and_types, me)

        log.info("Assert correct exception message")
        self.assertIn("User is already active on this record", str(cm.exception))

        log.info("Assert user has active order")
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertTrue(has_active_order)

        log.info("Assert no deadline on order")
        order = await crud_orders.get_order("1")
        self.assertIsNone(order["deadline"])

        log.info("Assert correct search results")
        orders_filter = crud_orders.OrderFilter(filter_status="active")
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

        log.info("Update order")
        update_values = {"comment": "Updated comment"}
        await crud_orders.update_order(order["order_id"], me["id"], update_values)

        log.info("Assert updated comment will not be added to log")
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 1)

        log.info("Move location of record to reading room")
        update_values = {"location": utils_orders.RECORD_LOCATION.READING_ROOM}
        await crud_orders.update_order(order["order_id"], me["id"], update_values)

        log.info("Order now has a deadline")
        order = await crud_orders.get_order("1")
        self.assertIsNotNone(order["deadline"])

        log.info("Assert 2 log messages (insert order and move location)")
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 2)

        with self.assertRaises(Exception) as cm:  # Capture the exception
            log.info("Move location of record if it is already in reading room. Should raise exception")
            update_values = {"location": utils_orders.RECORD_LOCATION.RETURN_TO_STORAGE}
            await crud_orders.update_order(order["order_id"], me["id"], update_values)

        log.info("Assert correct exception message")
        self.assertIn("Lokation kan ikke ændres", str(cm.exception))

        # Insert new order containing the same record as the first order but for another user
        log.info("Insert order for another user")
        await crud_orders.insert_order(meta_data, record_and_types, me_2)
        order_2 = await crud_orders.get_order("2")

        # check deadline
        self.assertIsNone(order_2["deadline"])

        log.info("Assert correct search results")
        orders_filter = crud_orders.OrderFilter(filter_status="active", filter_show_queued="on")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 2)

        log.info("User 1 completes order")
        update_values = {"order_status": utils_orders.ORDER_STATUS.COMPLETED}
        await crud_orders.update_order(order["order_id"], me["id"], update_values)

        log.info("Assert correct search results")
        orders_filter = crud_orders.OrderFilter(filter_status="active")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        orders_filter = crud_orders.OrderFilter(filter_status="completed")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        orders_filter = crud_orders.OrderFilter(filter_status="order_history")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        order_2 = await crud_orders.get_order("2")
        self.assertIsNotNone(order_2["deadline"])

        log.info("User 2 completes order")
        update_values = {"order_status": utils_orders.ORDER_STATUS.COMPLETED}
        await crud_orders.update_order(order_2["order_id"], me["id"], update_values)

        log.info("Order 2 assert 3 log messages (insert order, queued to ordered, ordered to completed)")
        logs = await crud_orders.get_logs("2")
        self.assertEqual(len(logs), 3)


if __name__ == "__main__":
    unittest.main()
