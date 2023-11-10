"""
Normalize a date in a strange way.
Copy of the original code.
"""

from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log


log = get_log()


def _split_date_str(date):
    # Alter a string date like 19570101 into 1957-01-01
    return f"{date[0:4]}-{date[4:6]}-{date[6:8]}"


def split_date_strings(record):
    """
    Split date strings in record
    """
    if "date_from" in record:
        record["date_from"] = _split_date_str(record["date_from"])
    if "date_to" in record:
        record["date_to"] = _split_date_str(record["date_to"])
    return record


def normalize_dates(record):
    """
    Add date_normalized to record
    """

    date_string = ""
    if record.get("date_from"):
        if record.get("date_to"):
            if record["date_to"] == record["date_from"]:
                date_string = record["date_from"]
            elif record["date_from"][0:7] == record["date_to"][0:7]:
                date_string = record["date_from"][0:7]
            elif record["date_from"][0:4] == record["date_to"][0:4] and record["date_from"][5:10] == "01-01":
                date_string = record["date_from"][0:4]
            elif record["date_from"][5:10] == "01-01" and record["date_to"][5:10] == "12-31":
                date_string = f"{record['date_from'][0:4]} ~ {record['date_to'][0:4]}"
            else:
                date_string = f"{record['date_from']} ~ {record['date_to']}"
        else:
            date_string = f"{record['date_from']} ~"
    elif record.get("date_to"):
        date_string = f"~ {record['date_to']}"
    else:
        date_string = translate("No Date")

    record["date_normalized"] = date_string
    return record


""" def _normalize_abstract_dates(record: dict):
    # This seems to be much simpler than the original code
    if "date_from" in record and "date_to" in record:
        date_from = record["date_from"]
        date_to = record["date_to"]
        if date_from == date_to:
            record["date_normalized"] = date_from
        else:
            record["date_normalized"] = date_from + " ~ " + date_to
    else:
        record["date_normalized"] = translate('No date')
    return record """
