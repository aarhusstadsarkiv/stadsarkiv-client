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
    Note: error_type, error_code, error_url are options in the python logger
    May use them at some point
    """
    try:
        data = await request.json()
        log.error(data.get("message", "JS ERROR"), extra={"exception": data.get("exception", "")})
        return JSONResponse({"status": "received"}, status_code=200)
    except Exception:
        log.error("No json data in request")
        return JSONResponse({"status": "received"}, status_code=200)
