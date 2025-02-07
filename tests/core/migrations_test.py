
from stadsarkiv_client.core.dynamic_settings import init_settings
from stadsarkiv_client.core.logging import get_log
import unittest
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.migrations.orders import migrations_orders

init_settings()
log = get_log()


class TestDB(unittest.TestCase):

    def test_migrations(self):
        db_path = ":memory:"
        migration = Migration(db_path=db_path, migrations=migrations_orders)
        migration.run_migrations()

        # Run again to test idempotency
        migration.run_migrations()


if __name__ == "__main__":
    unittest.main()
