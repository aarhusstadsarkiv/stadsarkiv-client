from maya.core.dynamic_settings import settings
from maya.core.logging import get_log

log = get_log()

try:
    database_url = settings["sqlite3"]["default"]
except KeyError:
    database_url = ""
