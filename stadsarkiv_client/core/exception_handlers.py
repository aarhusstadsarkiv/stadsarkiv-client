"""
Starlette Exception handlers for the application.
There is a default handler for 403, 404 and 500 errors.
"""

from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.auth import AuthException

HTML_403_PAGE = "403"
HTML_404_PAGE = "404"
HTML_500_PAGE = "500"

log = get_log()


async def not_found(request: Request, exc: HTTPException):
    context_values = {"title": translate("404 Not Found")}

    # No need to log full exception. It's a 404
    log.error(f"404 Not Found: {request.url}")
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=404)


async def server_error(request: Request, exc: HTTPException):
    context_values = {"title": translate("500 Server Error")}

    log.exception(f"500 Error: {request.url}", exc_info=exc)
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=500)


async def forbidden_error(request: Request, exc: HTTPException):
    context_values = {"title": translate("403 Forbidden Error")}

    log.error(f"403 Forbidden: {request.url}", exc_info=exc)
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=403)


async def auth_exception_handler(request: Request, exc: AuthException):
    flash.set_message(request, exc.message, type="error")
    return RedirectResponse(url=exc.redirect_url, status_code=302)


exception_handlers = {
    403: forbidden_error,
    404: not_found,
    500: server_error,
    AuthException: auth_exception_handler,
}
