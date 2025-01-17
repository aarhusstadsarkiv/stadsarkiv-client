"""
Utils for endpoints. 
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks import get_hooks

from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
import typing


log = get_log()


async def get_record_data(request: Request, record, permissions) -> typing.Tuple[dict, dict, dict]:

    """
    A mutated record is returned. In order to keep the original record make a copy before using this function.
    """
    hooks = get_hooks(request)

    meta_data = get_record_meta_data(request, record, permissions)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    record_altered = record_alter.record_alter(request, record, meta_data)
    record_and_types = record_alter.get_record_and_types(record_altered)

    record, record_and_types = await hooks.after_get_record_and_types(record, record_and_types)

    return record, meta_data, record_and_types
