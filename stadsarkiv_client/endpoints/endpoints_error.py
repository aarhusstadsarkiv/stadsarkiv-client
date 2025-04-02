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

        message = data.get("message", "")
        error_code = data.get("error_code", "")
        error_type = data.get("error_type", "")
        error_url = data.get("error_url", "")
        exception = data.get("exception", "")

        log.debug(f"Error url: {error_url}")

        # Compose extra fields for logging. Only add them if they are not empty
        extra = {}
        if error_code:
            extra["error_code"] = error_code
        if error_type:
            extra["error_type"] = error_type
        if error_url:
            extra["error_url"] = error_url
        if exception:
            extra["exception"] = exception

        log.error(message, extra=extra)
        return JSONResponse({"status": "received"}, status_code=200)
    except Exception:
        log.error("No json data in request")
        return JSONResponse({"status": "received"}, status_code=200)
