"""
Alter the record
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.records.normalize_abstract_dates import normalize_abstract_dates
from stadsarkiv_client.records.normalize_copyright_status import normalize_copyright_status
from stadsarkiv_client.records.normalize_contractual_status import normalize_contractual_status
from stadsarkiv_client.records.normalize_legal_restrictions import normalize_legal_restrictions
from stadsarkiv_client.records.normalize_availability import normalize_availability
from stadsarkiv_client.records.normalize_ordering import normalize_ordering
from stadsarkiv_client.records.normalize_record import normalize_record_data
from stadsarkiv_client.records.record_definitions import record_definitions

from starlette.requests import Request


log = get_log()


def record_alter(request: Request, record: dict, meta_data: dict):
    record = record.copy()

    record = normalize_record_data(record)
    record = normalize_abstract_dates(record)
    record = normalize_copyright_status(record, meta_data)
    record = normalize_contractual_status(record, meta_data)
    record = normalize_legal_restrictions(record, meta_data)
    record = normalize_availability(record, meta_data)
    record = normalize_ordering(record, meta_data)

    return record


def get_record_and_types(record):
    """
    Get record with types
    """
    record_altered = {}
    for key, value in record.items():
        record_item = {}
        record_item["value"] = value
        record_item["name"] = key

        try:
            definition = record_definitions[key]
            record_item["type"] = definition["type"]
            record_altered[key] = record_item
        except KeyError:
            pass

    return record_altered
