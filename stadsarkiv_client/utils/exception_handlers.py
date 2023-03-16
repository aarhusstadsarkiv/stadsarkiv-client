from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

HTML_403_PAGE = "403"
HTML_404_PAGE = "404"
HTML_500_PAGE = "500"


async def not_found(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)


async def server_error(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_500_PAGE, status_code=exc.status_code)


async def forbidden_error(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_403_PAGE, status_code=exc.status_code)


exception_handlers = {403: forbidden_error, 404: not_found, 500: server_error}
