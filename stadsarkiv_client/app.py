"""
Main application file for the stadsarkiv_client application.
"""

from starlette.applications import Starlette
from stadsarkiv_client.routes import get_routes
from stadsarkiv_client.core.middleware import middleware
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
log.debug(f"App loaded from the file {os.path.abspath(__file__)}")
routes = get_routes()

sentry_dns = os.getenv("SENTRY_DNS", "")
if sentry_dns:
    enable_sentry(sentry_dns)
    log.debug("Logging to sentry enabled")

app = Starlette(
    debug=settings["debug"],  # type: ignore
    middleware=middleware,
    routes=routes,
    exception_handlers=exception_handlers,  # type: ignore
)
