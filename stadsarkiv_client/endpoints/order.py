"""
Proxy for search records endpoints
"""

from starlette.requests import Request

# from starlette.responses import PlainTextResponse, JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log

# from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import api
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.records import record_alter
from stadsarkiv_client.records.meta_data_record import get_record_meta_data

# import json
from stadsarkiv_client.core.hooks import get_hooks
import asyncio

# from stadsarkiv_client.core.hooks import get_hooks


log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def order_get(request: Request):
    hooks = get_hooks(request)
    record_id = request.path_params["record_id"]

    permissions, record = await asyncio.gather(api.me_permissions(request), api.proxies_record_get_by_id(request, record_id))

    meta_data = get_record_meta_data(request, record)
    record, meta_data = await hooks.after_get_record(record, meta_data)

    record_altered = record_alter.record_alter(request, record, meta_data)
    record_and_types = record_alter.get_record_and_types(record_altered)

    data = {
        "record_id": record_id,
        "message": "test",
        "meta_data": meta_data,
        "is_employee": "employee" in permissions,
        "record_and_types": record_and_types,
    }

    context = await get_context(request, context_values=data)

    return templates.TemplateResponse("order/order.html", context)

    # return JSONResponse(data)
