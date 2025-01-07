"""
Webhook endpoints
"""

from starlette.responses import JSONResponse, HTMLResponse
from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.mail import get_template_content
from stadsarkiv_client.core import api
from stadsarkiv_client.core.dynamic_settings import settings


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
        data = "Error in mail_status"
        log.exception("Error in mail_status")

    return JSONResponse({"status": "ok", "data": data})


async def mail_verify_token(request: Request):
    """
    Mail status endpoint
    """

    # Test data
    data: dict = {
        "nonce": "ya_X5caNnPNNV8I1DRjogmHzO3xoKBn2OffA5M1we4c",
        "context": {},
        "original_request_id": "09c74815a76841d98da1268fdcb3b3e6",
        "error": None,
        "timestamp": 1736240547.001911,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk0NDAwMC00NDlhLTc0M2EtYjU4My0yNDJkMjNjMmNjZjgiLCJlbWFpbCI6IjAxOTQ0MDAwNDQ5NjcxMmVhODhiZmFlZjM2ODQ5MTY5QGludGVybmFsLmxvY2FsIiwiYXVkIjoiZmFzdGFwaS11c2Vyczp2ZXJpZnkiLCJleHAiOjE3MzYyNDQxNDZ9.dFuissS8vA7ZESmwPvH-aQy_Hn5zsY0Z4SJUhom9iY0",
        "to_user": {
            "id": "019265e5-3fd4-7734-990c-7c7660d1ca64",
            "email": "dennis.iversen+x@gmail.com",
            "is_active": True,
            "is_verified": False,
            "client_id": "demo",
            "display_name": "diversen",
            "data": {"bookmarks": [], "custom": {"updated": 1736240547, "data": {}}},
            "timestamp": 1736240546,
            "updated": 1736240546,
            "last_login": 1736240546,
            "permissions": [
                {"name": "user", "grant_id": 6, "entity_id": None},
                {"name": "guest", "grant_id": 8, "entity_id": None},
                {"name": "read", "grant_id": 9, "entity_id": None},
            ],
        },
    }

    # Get json data from request
    try:
        if request.method != "GET":
            data = await request.json()

        token = data["token"]
        user = data["to_user"]
        display_name = user["display_name"]

        template_values = {
            "display_name": display_name,
            "client_verify_url": settings["client_url"] + "/auth/verify/" + token,
            "client_domain_url": settings["client_url"],
            "client_name": settings["client_name"],
        }

        html_content = await get_template_content("mails/verify_email.html", template_values)

        user_id = user["id"]

        mail_dict = {
            "data": {
                "user_id": user_id,
                "subject": "Bekræft din konto",
                "sender": {"email": "stadsarkivet@aarhusarkivet.dk", "name": "Aarhus Stadsarkiv"},
                "reply_to": {"email": "stadsarkivet@aarhusarkivet.dk", "name": "Aarhus Stadsarkiv"},
                "html_content": html_content,
                "text_content": html_content,
            }
        }

        await api.mail_post(request, mail_dict)
        log.info(f"Verify email sent to: {user['email']}")
    except Exception:
        data = "Error in mail_status"
        log.exception("Error in sending verify email to user")

    return JSONResponse({"status": "ok", "data": data})


async def mail_reset_token(request: Request):
    """
    Mail status endpoint
    """
    # Get json data from request
    try:
        data = await request.json()
        log.info(data)
    except Exception:
        data = "Error in mail_status"
        log.exception("Error in mail_status")

    return JSONResponse({"status": "ok", "data": data})
