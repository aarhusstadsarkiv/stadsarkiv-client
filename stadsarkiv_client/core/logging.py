from typing import Any
import logging
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import logging_defs
import warnings
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import os

warnings.simplefilter(action="ignore", category=FutureWarning)


log = logging.getLogger("main")
level: Any = settings["log_level"]
log.setLevel(level)


def enable_sentry(sentry_dns: str):
    # All of this is already happening by default!
    sentry_logging = LoggingIntegration(
        level=level, event_level=level  # Capture info and above as breadcrumbs  # Send warnings as events
    )

    # assert in order to remove type warning
    assert (sentry_logging is not None)

    if sentry_dns:
        log.debug("Sentry DNS: " + str(sentry_dns))
        sentry_sdk.init(
            dsn=sentry_dns,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )


sentry_dns = os.getenv("SENTRY_DNS", "")
if sentry_dns:
    enable_sentry(sentry_dns)


class customHandler(logging.Handler):
    def emit(self, record):
        pass


if not len(log.handlers):
    # log.addHandler(customHandler())
    if "file" in settings["log_handlers"]:  # type: ignore
        logging_defs.generate_log_dir()
        fh = logging_defs.get_file_handler(level)
        log.addHandler(fh)

    if "stream" in settings["log_handlers"]:  # type: ignore
        ch = logging_defs.get_stream_handler(level)
        log.addHandler(ch)


def get_log() -> logging.Logger:
    return log
