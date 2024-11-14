from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.crud import CRUD

log = get_log()

try:
    database_url = settings["sqlite3"]["orders"]
except KeyError:
    database_url = ""

crud_orders = CRUD(database_url=database_url, table="orders")
