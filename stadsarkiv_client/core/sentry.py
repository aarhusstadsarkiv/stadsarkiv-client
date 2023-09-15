"""
Enables sentry logging for the stadsarkiv_client package.
"""

from stadsarkiv_client.core.dynamic_settings import settings
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def enable_sentry(sentry_dns: str):
    # All of this is already happening by default!
    sentry_level = settings["sentry_level"]
    sentry_event_level = settings["sentry_event_level"]
    sentry_logging = LoggingIntegration(
        level=sentry_level, event_level=sentry_event_level  # Capture info and above as breadcrumbs  # Send warnings as events
    )

    # assert in order to remove type warning
    assert sentry_logging is not None

    sentry_sdk.init(
        dsn=sentry_dns,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )
