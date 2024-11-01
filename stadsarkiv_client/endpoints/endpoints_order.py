"""
Proxy for search records endpoints
"""

from starlette.requests import Request
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core import api
from stadsarkiv_client.core.auth import is_authenticated
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data
from stadsarkiv_client.core.hooks import get_hooks
from stadsarkiv_client.database import orders
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import asyncio


log = get_log()


async def orders_get_order(request: Request):
    await is_authenticated(request)

    me = await api.users_me_get(request)
    # log.debug(me)

    hooks = get_hooks(request)
    record_id = request.path_params["record_id"]

    permissions, record = await asyncio.gather(api.me_permissions(request), api.proxies_record_get_by_id(request, record_id))

    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    # storage_id, barcode, location = orders.get_info_from_record(record)

    # uden location kan materiale ikke bestilles. 

    
    # # log.debug(storage_id, barcode, location)

    # log.debug(storage_id)
    # log.debug(barcode)
    # log.debug(location)

    # log.debug(meta_data)

    # insert_values = {
    #     "user_id": me["id"],
    #     "record_id": meta_data["real_id"],

    # }


    # log.debug(f"meta_data: {meta_data}")
    # log.debug(f"record: {record}")


    # # await orders.orders_insert({"record_id": "000503354", "user_id": "1", "identifier": "51648293"})

    # record_altered = record_alter.record_alter(request, record, meta_data)
    # record_and_types = record_alter.get_record_and_types(record_altered)

    # context_variables = {
    #     "is_employee": "employee" in permissions,
    #     "title": "Bestil: " + meta_data["title"],
    #     "meta_title": "Bestil: " + meta_data["meta_title"],
    #     "meta_data": meta_data,
    #     "record_and_types": record_and_types,
    # }

    # context = await get_context(request, context_values=context_variables)

    # return templates.TemplateResponse(request, "order/order.html", context)


async def orders_post(request: Request):
    pass
