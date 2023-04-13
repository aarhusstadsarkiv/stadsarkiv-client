from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core import flash
from stadsarkiv_client.core import api
from stadsarkiv_client.core.api import OpenAwsException
import json
from stadsarkiv_client.core.openaws import (
    SchemaRead,
    EntityRead,
    RecordsIdGet,
)


log = get_log()


@is_authenticated(message=translate("You need to be logged in to view this page."), permissions=["admin"])
async def get_record_view(request: Request):
    try:
        record: RecordsIdGet = await api.record_read(request)
        record_dict = record.to_dict()

        record_json = json.dumps(record_dict, indent=4, ensure_ascii=False)

        context_values = {"title": translate("Entity"), "record": record_json}

        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/record.html", context)

    except Exception as e:
        # for sure this is a 404
        raise HTTPException(404, detail=str(e), headers=None)
