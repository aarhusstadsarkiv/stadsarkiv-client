from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log


log = get_log()


async def post(request: Request):

    # Get form data
    data = await request.form()
    log.debug(f"Data: {data}")

    return JSONResponse({"message": "Hello, World!"})
