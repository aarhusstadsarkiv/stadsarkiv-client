"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.database import cache
import random

log = get_log()


async def test_get(request: Request):

    # await database.bookmarks_insert("Test note", "UUID-1234")
    insert_value = None
    # Get a result that is max 10 seconds old
    cache_expire = 10
    has_result = False
    result = await cache.cache_get("test", cache_expire)

    if not result:
        # Set a new cache value
        insert_value = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        await cache.cache_set("test", {"random": insert_value})
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
