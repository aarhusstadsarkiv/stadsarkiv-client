"""
Error endpoints.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log

log = get_log()


async def error_log_post(request: Request):
    """
    Log posted json data
    """

    try:
        data = await request.json()
        log.error(data)
        return JSONResponse({"status": "received"}, status_code=200)
    except Exception:
        log.error("No json data in request")
        return JSONResponse({"status": "received"}, status_code=200)
