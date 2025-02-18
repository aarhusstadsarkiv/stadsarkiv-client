from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from stadsarkiv_client.database.crud_orders import cron_orders_expire
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.dynamic_settings import settings
import asyncio

log = get_log()


def run_cron_orders():
    """
    Run the cron job for orders
    """
    log.info("Running async cron job")
    try:
        asyncio.run(cron_orders_expire())
    except Exception:
        log.exception("Cron job failed")
    log.info("Async cron job completed")


# Initialize scheduler
scheduler = BackgroundScheduler()
if settings.get("environment") == "development":
    log.info("Running cron job every minute in development")
    scheduler.add_job(run_cron_orders, "cron", minute="*")
else:
    log.info("Running cron job every day at midnight")
    scheduler.add_job(run_cron_orders, "cron", hour=0, minute=0)

scheduler.start()
