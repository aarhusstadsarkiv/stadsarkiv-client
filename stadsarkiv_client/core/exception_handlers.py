"""
Starlette Exception handlers for the application.
There is a default handler for 403, 404 and 500 errors.
"""

from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.auth import AuthException, AuthExceptionJSON
from httpx import HTTPStatusError
import traceback

HTML_403_PAGE = "403"
HTML_404_PAGE = "404"
HTML_500_PAGE = "500"

log = get_log()


async def not_found(request: Request, exc: HTTPException):
    """
    404 Not Found error.
    """
    context_values = {
        "title": f"404 {translate('Error. Not Found')}",
        "status_code": 404,
        "human_error": "Siden du leder efter findes ikke. ",
    }

    # No need to log full exception. It's a 404
    log.warning(f"404 Not Found: {request.url}", extra={"error_code": 404, "error_url": request.url})
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=404)


async def http_status_error(request: Request, exc: HTTPStatusError):
    """
    Any HTTP status error that is not caught by the application.
    """

    exc_traceback = traceback.format_exc()
    title = f"{exc.response.status_code}. {translate('Error. Request Error')}"
    context_values = {
        "title": title,
        "status_code": exc.response.status_code,
        "human_error": (
            "Der skete en fejl, da systemet hentede data fra et API. Fejlen er blevet logget, og vi vil kigge på det hurtigst muligt."
        ),
        "exc": exc,
        "exc_traceback": exc_traceback,
    }

    extra = {"error_code": exc.response.status_code, "error_url": request.url}
    log.exception(f"{exc.response.status_code} Error: {request.url}", extra=extra)
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=exc.response.status_code)


async def server_error(request: Request, exc: Exception):
    """
    Any 500 error that is not caught by the application.
    """

    exc_traceback = traceback.format_exc()
    context_values = {
        "title": f"500 {translate('Error. Server Error')}",
        "status_code": 500,
        "human_error": "Der skete en system fejl. Fejlen er blevet logget og vi vil kigge på det hurtigst muligt.",
        "exc": exc,
        "exc_traceback": exc_traceback,
    }

    extra = {"error_code": 500, "error_url": request.url}
    log.exception(f"500 Error: {request.url}", extra=extra)
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=500)


async def forbidden_error(request: Request, exc: HTTPException):
    """
    403 Forbidden error.
    """

    context_values = {
        "title": translate("Error. Forbidden Error"),
        "status_code": 403,
        "human_error": "Du har ikke adgang til denne side. Fejlen er blevet logget. ",
    }

    log.exception(f"403 Forbidden: {request.url}")
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "errors/default.html", context, status_code=403)


async def auth_exception_handler(request: Request, exc: AuthException):
    """
    AuthException handler for 403 Forbidden.
    """
    flash.set_message(request, exc.message, type="error")
    log.exception(f"403 Forbidden: {request.url}")
    log.info(f"AuthException Redirect to: {exc.redirect_url}")
    return RedirectResponse(url=exc.redirect_url, status_code=302)


async def auth_exception_json_handler(request: Request, exc: AuthExceptionJSON):
    """
    AuthException handler for 403 Forbidden with JSON response.
    """
    return JSONResponse({"error": True, "message": exc.message}, status_code=401)


exception_handlers = {
    403: forbidden_error,
    404: not_found,
    500: server_error,
    HTTPStatusError: http_status_error,
    AuthException: auth_exception_handler,
    AuthExceptionJSON: auth_exception_json_handler,
}
