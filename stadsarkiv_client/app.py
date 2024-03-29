"""
Main application file for the stadsarkiv_client application.
"""

from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.core import middleware
from stadsarkiv_client.core.exception_handlers import exception_handlers
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.sentry import enable_sentry
import os
import json

log = get_log()

log.debug("Environment: " + str(os.getenv("ENVIRONMENT")))
log.debug(json.dumps(settings, sort_keys=True, indent=4, ensure_ascii=False))

# Log absolute path to this file (in case we use the pipx version)
log.debug("App loaded from the file " + os.path.abspath(__file__))

sentry_dns = os.getenv("SENTRY_DNS", "")
if sentry_dns:
    enable_sentry(sentry_dns)
    log.debug("Logging to sentry enabled")

app = Starlette(
    debug=settings["debug"],  # type: ignore
    middleware=[
        middleware.cors_middleware,
        middleware.first_middleware,
        middleware.session_middleware,
        middleware.session_autoload_middleware,
        middleware.last_middleware,
        middleware.no_cache_middleware,
        middleware.gzip_middleware,
    ],
    routes=routes,
    exception_handlers=exception_handlers,  # type: ignore
)
