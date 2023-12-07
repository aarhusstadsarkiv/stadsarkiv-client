"""
Just a test endpoint in order to test anything
Only enabled in development mode
"""

from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.templates import templates
import random


log = get_log()


async def test_default(request: Request):
    # https://placehold.co/600x400
    # generate a context containing 10 images with random sizes.
    # But min width is 200px and max width is 360px
    # The height maybe between 50px and 600px

    # random_images is a list of strings
    random_images = []
    for _ in range(20):
        width = random.randint(200, 360)
        height = random.randint(50, 600)
        random_images.append(f"https://placehold.co/{width}x{height}")

    context_values = {"title": "Base test page", "random_images": random_images}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse("testing/test.html", context)


async def test_page(request: Request):
    # get page id from request
    page = request.path_params["page"]
    context_values = {"title": f"Test page: {page}"}
    context = await get_context(request, context_values=context_values)

    return templates.TemplateResponse(f"testing/{page}.html", context)


async def test_post(request: Request):
    # get POST data
    # data = await request.form()
    form = await request.form()
    data = {k: v for k, v in form.items() if k != "upload-file"}  # the form data except the file
    return JSONResponse({"data": data})
