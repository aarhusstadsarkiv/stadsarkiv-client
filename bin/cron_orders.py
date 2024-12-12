import os
from stadsarkiv_client.database.crud_orders import cron_orders
from stadsarkiv_client.core.logging import get_custom_log
import asyncio


log = get_custom_log("cron_orders", "cron_orders.log")

# Set the environment variable in the script
os.environ["CONFIG_DIR"] = "example-config-aarhus"

# Use the CONFIG_DIR in your script
config_dir = os.getenv("CONFIG_DIR")
print(f"Using configuration directory: {config_dir}")

log.debug(f"Using configuration directory: {config_dir}")

asyncio.run(cron_orders())
