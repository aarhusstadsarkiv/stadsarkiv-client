"""
Error endpoints.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log

log = get_log()


async def error_log_post(request: Request):
    """
    Log posted JSON data.

    Note: The caller is responsible for providing a meaningful 'message'.
    Optional fields: error_code, error_type, error_url, exception
    """

    try:
        data = await request.json()

        extra = {
            "error_code": data.get("error_code", 500),
            "error_type": data.get("error_type", "UnknownError"),
            "error_url": data.get("error_url", str(request.url.path)),
            "exception": data.get("exception", ""),
        }

        log.error(data.get("message"), extra=extra)
        return JSONResponse({"status": "received"}, status_code=200)

    except Exception as e:

        extra = {"error_code": 500, "error_type": "UnknownError", "error_url": str(request.url.path), "exception": str(e)}

        log.error("Failed to parse error log", extra=extra)
        return JSONResponse({"status": "received"}, status_code=200)
