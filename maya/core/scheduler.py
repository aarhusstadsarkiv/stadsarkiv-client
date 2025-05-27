"""
This module sets up and manages background cron jobs using APScheduler to handle
asynchronous maintenance tasks in the Maya application. Specifically, it schedules
and runs two cron jobs:

1. `cron_orders_expire`: Handles the expiration of orders.
2. `cron_renewal_emails`: Sends out renewal reminder emails.

The scheduler is configured based on application settings:
- In a development environment, both jobs run every minute.
- In other environments (e.g., production), the jobs run daily at specified times:
  - Orders expiration at 00:02 AM.
  - Renewal emails at 00:04 AM.

All scheduled tasks are wrapped with logging and error handling to capture job status
and exceptions during execution. Async functions are executed using `asyncio.run`.
"""

from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from maya.database.crud_orders import cron_orders_expire, cron_renewal_emails
from maya.core.logging import get_log
from maya.core.dynamic_settings import settings
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

# Cron orders if enabled
if settings.get("cron_orders", False):
    if settings.get("environment") == "development":
        log.info("Running cron job every minute in development")
        scheduler.add_job(run_cron_orders_expire, "cron", minute="*")
        scheduler.add_job(run_cron_renewal_emails, "cron", minute="*")
    else:
        log.info("Running cron job every day at midnight")
        scheduler.add_job(run_cron_orders_expire, "cron", hour=0, minute=2)
        scheduler.add_job(run_cron_renewal_emails, "cron", hour=0, minute=4)


scheduler.start()
