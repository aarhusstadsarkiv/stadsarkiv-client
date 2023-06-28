from datetime import datetime
from babel.dates import format_datetime
import locale


locale.setlocale(locale.LC_ALL, "da_DK.UTF-8")


def format_date(date_string: str) -> str:
    """Format a date string to a Danish format"""
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    date = datetime.strptime(date_string, date_format)
    formatted_date = format_datetime(date, format="d. MMMM y HH:mm", locale="da_DK")
    return formatted_date
