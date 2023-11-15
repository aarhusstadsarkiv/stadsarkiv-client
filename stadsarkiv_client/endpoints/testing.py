"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.templates import templates


log = get_log()


async def test(request: Request):
    context_values = {"title": "TEST"}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse("testing/test.html", context)


async def test_post(request: Request):
    # get POST data
    # data = await request.form()
    form = await request.form()
    data = {k: v for k, v in form.items() if k != "upload-file"}  # the form data except the file
    return JSONResponse({"data": data})
