"""
Format a date string to a Danish format
"""

from datetime import datetime
from babel.dates import format_datetime, format_date
from stadsarkiv_client.core.logging import get_log
from zoneinfo import ZoneInfo

log = get_log()


def timezone_alter(utc_timestamp: str, target_timezone: str = "Europe/Copenhagen") -> str:
    """
    Convert utc timestamp to a target timezone
    E.g. convert a sql timestamp like '2024-11-19 11:25:58' to 'Europe/Copenhagen' and get e.g. '2024-11-19 12:25:58'
    """
    utc_dt = datetime.strptime(utc_timestamp, "%Y-%m-%d %H:%M:%S")
    utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    target_dt = utc_dt.astimezone(ZoneInfo(target_timezone))

    return str(target_dt.replace(tzinfo=None))


def date_format(date_string: str) -> str:
    """
    Format a date string to a Danish format
    """
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
    """
    Format a date string to a Danish format
    """
    try:
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date_string, date_format)
        formatted_date = format_date(date, format="d. MMMM y", locale="da_DK")
        return formatted_date
    except Exception:
        log.exception("Error in date_format_day")
        return date_string


def _sanitize_date_string(date_string: str) -> str:
    """
    remove microseconds from date string
    so that it can be parsed by datetime.strptime as "%Y-%m-%dT%H:%M:%S"
    Some dates comes as the format "%Y-%m-%dT%H:%M:%S.%f"
    """
    if "." in date_string:
        return date_string.split(".")[0]
    return date_string
