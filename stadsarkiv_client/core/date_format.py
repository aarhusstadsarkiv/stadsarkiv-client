"""
Format a date string to a Danish format
"""

from datetime import datetime
from babel.dates import format_datetime, format_date
import locale
from stadsarkiv_client.core.logging import get_log


log = get_log()


locale.setlocale(locale.LC_ALL, "da_DK.UTF-8")


def _sanitize_date_string(date_string: str) -> str:
    """remove microseconds from date string
    so that it can be parsed by datetime.strptime as "%Y-%m-%dT%H:%M:%S"
    Some dates comes as the format "%Y-%m-%dT%H:%M:%S.%f"
    """
    if "." in date_string:
        return date_string.split(".")[0]
    return date_string


def date_format(date_string: str) -> str:
    """Format a date string to a Danish format"""
    try:
        date_format = "%Y-%m-%dT%H:%M:%S"
        date_string = _sanitize_date_string(date_string)
        date = datetime.strptime(date_string, date_format)
        formatted_date = format_datetime(date, format="d. MMMM y HH:mm", locale="da_DK")
        return formatted_date
    except Exception:
        log.exception("Error in date_format")
        return date_string


def date_format_day(date_string: str) -> str:
    """Format a date string to a Danish format"""
    try:
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date_string, date_format)
        formatted_date = format_date(date, format="d. MMMM y", locale="da_DK")
        return formatted_date
    except Exception:
        log.exception("Error in date_format_day")
        return date_string
