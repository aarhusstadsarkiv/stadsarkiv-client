"""
Webhook endpoints
"""

from starlette.responses import JSONResponse
from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log


log = get_log()


async def mail_status(request: Request):
    """
    Mail status endpoint
    """

    # Get json data from request
    try:
        data = await request.json()
        log.info(data)
    except Exception:
        log.error("Error in mail_status")

    return JSONResponse({"status": "ok"})


async def mail_verify_token(request: Request):
    """
    Mail status endpoint
    """

    # Get json data from request
    try:
        data = await request.json()
        log.info(data)
    except Exception:
        log.error("Error in mail_status")

    return JSONResponse({"status": "ok"})


async def mail_reset_token(request: Request):
    """
    Mail status endpoint
    """
    # Get json data from request
    try:
        data = await request.json()
        log.info(data)
    except Exception:
        log.error("Error in mail_status")

    return JSONResponse({"status": "ok"})
