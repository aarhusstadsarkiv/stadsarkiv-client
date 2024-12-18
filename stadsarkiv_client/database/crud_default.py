from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log

log = get_log()

try:
    database_url = settings["sqlite3"]["default"]
except KeyError:
    database_url = ""
