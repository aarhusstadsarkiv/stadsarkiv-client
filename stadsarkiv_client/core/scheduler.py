from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from stadsarkiv_client.database.crud_orders import cron_orders_expire, cron_renewal_emails
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.dynamic_settings import settings
import asyncio

log = get_log()


def run_cron_orders_expire():
    """
    Run the cron job for orders
    """
    log.info("Running async cron job")
    try:
        asyncio.run(cron_orders_expire())
    except Exception:
        log.exception("Cron job failed")
    log.info("Async cron job completed")


def run_cron_renewal_emails():
    """
    Run the cron job for renewal emails
    """
    log.info("Running async cron job")
    try:
        asyncio.run(cron_renewal_emails())
    except Exception:
        log.exception("Cron job failed")
    log.info("Async cron job completed")


# Initialize scheduler
scheduler = BackgroundScheduler()
if settings.get("environment") == "development":
    log.info("Running cron job every minute in development")
    scheduler.add_job(run_cron_orders_expire, "cron", minute="*")
    scheduler.add_job(run_cron_renewal_emails, "cron", minute="*")
else:
    log.info("Running cron job every day at midnight")
    scheduler.add_job(run_cron_orders_expire, "cron", hour=0, minute=2)
    scheduler.add_job(run_cron_renewal_emails, "cron", hour=0, minute=4)



scheduler.start()
