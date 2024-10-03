"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.templates import templates
import sqlite3
import os
import typing


DATABASE_URL = str(os.getenv("DATABASE_URL"))


log = get_log()


async def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


async def test_get(request: Request):

    await insert_bookmark("Test note", "UUID-1234")
    return JSONResponse({"message": "Test note inserted"})


async def insert_bookmark(bookmark, user_id) -> typing.Any:

    connection = await get_db_connection()
    cursor = connection.cursor()

    try:

        values = {"user_id": user_id, "bookmark": "bookmark"}
        query = "INSERT INTO bookmarks (user_id, bookmark) VALUES (:user_id, :bookmark)"
        cursor.execute(query, values)
        connection.commit()

    except sqlite3.Error as e:
        log.error(f"Failed to insert note: {e}")
        connection.rollback()
    finally:
        cursor.close()


async def test_page(request: Request):
    # get page id from request
    page = request.path_params["page"]
    context_values = {"title": f"Test page: {page}"}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(request, f"testing/{page}.html", context)


async def test_post(request: Request):
    context = await get_context(request)
    return templates.TemplateResponse(request, "testing/thanks.html", context)
