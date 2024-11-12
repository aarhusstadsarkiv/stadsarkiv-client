from stadsarkiv_client.database.crud import CRUD
from stadsarkiv_client.core.logging import get_log


log = get_log()
bookmarks_crud = CRUD(database="default", table="bookmarks")
