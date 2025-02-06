"""
Main application file for the stadsarkiv_client application.
"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from starlette.applications import Starlette
from stadsarkiv_client.routes import get_app_routes
from stadsarkiv_client.core.middleware import middleware
from stadsarkiv_client.core.exception_handlers import exception_handlers
from stadsarkiv_client.core.sentry import enable_sentry
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.core.args import get_data_dir
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from stadsarkiv_client.database.crud_orders import cron_orders
import asyncio
import contextlib
import os
import sys

sys.path.append(".")
log = get_log()
data_dir = get_data_dir()

if not os.path.exists(data_dir):
    log.info(f"Creating data directory: {data_dir}")
    os.makedirs(data_dir)

api_key = settings.get("api_key")
if api_key == "api_key":
    raise ValueError("API_KEY environment variable is not set")

log.info("Environment: " + str(settings.get("environment")))
log.info(f"App loaded from the file {os.path.abspath(__file__)}")

hooks = get_hooks()
routes = get_app_routes()
routes = hooks.after_routes_init(routes)


def run_cron_orders():
    """
    Run the cron job for orders
    """
    log.info("Running async cron job")
    try:
        asyncio.run(cron_orders())
    except Exception:
        log.exception("Cron job failed")

    log.info("Async cron job completed")


# Set up the scheduler
scheduler = BackgroundScheduler()
if settings.get("environment") == "development":
    scheduler.add_job(run_cron_orders, "cron", minute="*")
else:
    scheduler.add_job(run_cron_orders, "cron", hour=0, minute=0)

scheduler.start()


sentry_dns = os.getenv("SENTRY_DNS", "")
if sentry_dns:
    enable_sentry(sentry_dns)
    log.debug("Logging to sentry enabled")


@contextlib.asynccontextmanager
async def lifespan(app):

    try:
        log.info("App lifecycle started")
        yield
    finally:
        scheduler.shutdown()
        log.info("App lifecycle ended")


app = Starlette(
    debug=settings["debug"],  # type: ignore
    middleware=middleware,
    routes=routes,
    exception_handlers=exception_handlers,  # type: ignore
    lifespan=lifespan,
)
