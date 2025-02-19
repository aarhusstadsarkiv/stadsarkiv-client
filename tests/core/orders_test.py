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

        # Generate a new database for testing
        db_path = "/tmp/orders.db"
        if os.path.exists(db_path):
            os.remove(db_path)

        migration = Migration(db_path=db_path, migrations=migrations_orders)
        migration.run_migrations()

        # Load user, meta_data and record_and_types - test data
        me_data_file = "tests/data/me.json"
        with open(me_data_file) as f:
            me = json.load(f)

        meta_data_file = "tests/data/meta_data_000495102.json"
        with open(meta_data_file) as f:
            meta_data = json.load(f)

        record_and_types_file = "tests/data/record_and_types_000495102.json"
        with open(record_and_types_file) as f:
            record_and_types = json.load(f)

        # Generate a second user
        me_2 = me.copy()
        me_2["id"] = "ANOTHER_USER_ID"
        me_2["email"] = "another.email@example.com"

        # Test has_active_order
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertFalse(has_active_order)

        # Test insert_order
        await crud_orders.insert_order(meta_data, record_and_types, me)

        # Test exception if user is already active on this record
        with self.assertRaises(Exception) as cm:
            await crud_orders.insert_order(meta_data, record_and_types, me)

        self.assertIn("User is already active on this record", str(cm.exception))

        # Test has_active_order again with the new order
        has_active_order = await crud_orders.has_active_order(me["id"], meta_data["id"])
        self.assertTrue(has_active_order)

        # Test no expire_at
        order = await crud_orders.get_order(1)

        # Test is user is owner
        is_owner = await crud_orders.is_owner(me["id"], order["order_id"])
        self.assertTrue(is_owner)

        # Check that order does not have an expire_at
        self.assertIsNone(order["expire_at"])

        # Test for correct filters results
        orders_filter = crud_orders.OrderFilter(filter_status="active")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        orders_filter = crud_orders.OrderFilter(filter_status="completed")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        orders_filter = crud_orders.OrderFilter(filter_status="order_history")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        # Test correct amount of log messages
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 1)

        # Test update_order comment
        update_values = {"comment": "Updated comment"}
        await crud_orders.update_order(
            me["id"],
            order["order_id"],
            update_values,
        )

        # Update comment is not added to the log
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 1)

        # Update location to reading room
        update_values = {"location": utils_orders.RECORD_LOCATION.READING_ROOM}
        await crud_orders.update_order(
            me["id"],
            order["order_id"],
            update_values,
        )

        # Order should now have an expire_at
        order = await crud_orders.get_order("1")
        self.assertIsNotNone(order["expire_at"])

        # Test correct amount of log messages
        logs = await crud_orders.get_logs("1")
        self.assertEqual(len(logs), 2)

        # Test that location can not be changed when order is active and in reading room
        with self.assertRaises(Exception) as cm:
            update_values = {"location": utils_orders.RECORD_LOCATION.RETURN_TO_STORAGE}
            await crud_orders.update_order(
                me["id"],
                order["order_id"],
                update_values,
            )

        # Test correct exception message
        self.assertIn("Lokation kan ikke ændres", str(cm.exception))

        # Insert new order containing the same record as the first order but for another user
        await crud_orders.insert_order(meta_data, record_and_types, me_2)
        order_2 = await crud_orders.get_order("2")

        # Check if order_2 status is queued
        self.assertEqual(order_2["order_status"], utils_orders.ORDER_STATUS.QUEUED)

        # check expire_at
        self.assertIsNone(order_2["expire_at"])

        # Test correct of filter results
        orders_filter = crud_orders.OrderFilter(filter_status="active", filter_show_queued="on")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 2)

        # User 1 completes order
        update_values = {"order_status": utils_orders.ORDER_STATUS.COMPLETED}
        await crud_orders.update_order(
            me["id"],
            order["order_id"],
            update_values,
        )

        # Check filter results
        orders_filter = crud_orders.OrderFilter(filter_status="active")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        orders_filter = crud_orders.OrderFilter(filter_status="completed")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 0)

        orders_filter = crud_orders.OrderFilter(filter_status="order_history")
        orders, _ = await crud_orders.get_orders_admin(filters=orders_filter)
        self.assertEqual(len(orders), 1)

        # User 2 should get an expire_at now. As the record is in reading room
        order_2 = await crud_orders.get_order("2")
        self.assertIsNotNone(order_2["expire_at"])

        log.info("User 2 completes order")
        update_values = {"order_status": utils_orders.ORDER_STATUS.COMPLETED}
        await crud_orders.update_order(
            me["id"],
            order_2["order_id"],
            update_values,
        )

        log.info("Order 2 assert 3 log messages (insert order, queued to ordered, ordered to completed)")
        logs = await crud_orders.get_logs("2")
        self.assertEqual(len(logs), 3)


if __name__ == "__main__":
    unittest.main()
