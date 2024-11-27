from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log

log = get_log()

try:
    default_url = settings["sqlite3"]["default"]
except KeyError:
    default_url = ""

crud_default = CRUD(database_url=default_url)
