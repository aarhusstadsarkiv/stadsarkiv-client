from starlette.requests import Request
from stadsarkiv_client.utils.logging import get_log


log = get_log()


async def get_user(request: Request):
    log.debug("get_user")
    pass
