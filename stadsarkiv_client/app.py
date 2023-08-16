from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.core.middleware import session_middleware, session_autoload_middleware
from stadsarkiv_client.core.exception_handlers import exception_handlers
import os
import json
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
import sentry_sdk


log = get_log()

log.debug("Environment: " + str(os.getenv("ENVIRONMENT")))
log.debug(json.dumps(settings, sort_keys=True, indent=4, ensure_ascii=False))

sentry_dns = os.getenv('SENTRY_DNS')

if sentry_dns:

    log.info("Sentry DNS: " + str(sentry_dns))
    sentry_sdk.init(
        dsn=sentry_dns,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )

app = Starlette(
    debug=settings["debug"],  # type: ignore
    middleware=[session_middleware, session_autoload_middleware],
    routes=routes,
    exception_handlers=exception_handlers,  # type: ignore
)
