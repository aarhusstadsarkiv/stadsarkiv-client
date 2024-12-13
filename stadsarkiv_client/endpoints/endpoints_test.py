"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.database.cache import DatabaseCache
from stadsarkiv_client.database.crud_default import database_url
from stadsarkiv_client.database.utils import DatabaseConnection
from stadsarkiv_client.core import api
import random

log = get_log()


async def test_get(request: Request):

    insert_value = None
    # Get a result that is max 10 seconds old
    cache_expire = 10
    has_result = False

    database_connection = DatabaseConnection(database_url)
    async with database_connection.transaction_scope_async() as connection:
        cache = DatabaseCache(connection)
        result = await cache.get("test", cache_expire)

        if not result:
            # Set a new cache value
            insert_value = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
            await cache.set("test", {"random": insert_value})
        else:
            has_result = True

    return JSONResponse(
        {
            "message": "Test note inserted",
            "result": result,
            "has_result": has_result,
            "expire": cache_expire,
            "inserted_value": insert_value,
        }
    )


async def test_page(request: Request):
    # get page id from request
    page = request.path_params["page"]
    context_values = {"title": f"Test page: {page}"}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, f"testing/{page}.html", context)


async def test_post(request: Request):
    context = await get_context(request)
    return templates.TemplateResponse(request, "testing/thanks.html", context)


# from stadsarkiv_client.core.dataclasses import Mail


async def test_mail(request: Request):

    context_values = {
        "display_name": "Test User",
        "CLIENT_EMAIL_VERIFY_DOMAIN_URL": "https://verify.openaws.dk",
        "token": "123456",
        "CLIENT_DOMAIN_URL": "https://demo.openaws.dk",
        "CLIENT_NAME": "Demo",
    }

    context = await get_context(request, context_values=context_values)

    # template_str = await get_template_content("mails/verify_email.html", context)

    data_dict = {
        "data": {
            "user_id": "019265e5-3fd4-7734-990c-7c7660d1ca64",
            "subject": "Test",
            "sender": {"email": "stadsarkivet@aarhusarkivet.dk", "name": "Aarhus Stadsarkiv"},
            "reply_to": {"email": "stadsarkivet@aarhusarkivet.dk", "name": "Aarhus Stadsarkiv"},
            "html_content": "Test Test",
            "text_content": "Test Test",
        }
    }

    await api.mail_post(request, data_dict)

    return templates.TemplateResponse(request, "mails/verify_email.html", context)
