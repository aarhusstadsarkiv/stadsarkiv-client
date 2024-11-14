from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log


log = get_log()

try:
    database_url = settings["sqlite3"]["default"]
except KeyError:
    database_url = ""

crud_bookmarks = CRUD(database_url=database_url, table="bookmarks")
