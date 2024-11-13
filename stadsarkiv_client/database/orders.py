from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.crud import CRUD

log = get_log()
database_url = settings["sqlite3"]["orders"]
orders_crud = CRUD(database_url=database_url, table="orders")
