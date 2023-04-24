from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, PlainTextResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.core import alter_record
from stadsarkiv_client.core.openaws import (
    SchemaRead,
    EntityRead,
    RecordsIdGet,
)


log = get_log()


async def get_records_search(request: Request):
    try:
        context_values = {"title": translate("Search")}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/search.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)


async def get_records_search_results(request: Request):
    try:
        context_values = {"title": translate("Search results")}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/search.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)


async def get_record_view(request: Request):
    try:
        record: RecordsIdGet = await api.record_read(request)

        record_dict = record.to_dict()

        record_dict = alter_record.alter_record(record_dict)
        record_json = json.dumps(record_dict, indent=4, ensure_ascii=False)

        record_sections = alter_record.get_sections(record_dict)
        record_sections_json = json.dumps(record_sections, indent=4, ensure_ascii=False)

        image = alter_record.get_record_image(record_dict)
        if image:
            record_dict["image"] = alter_record.get_record_image(record_dict)
        else:
            record_dict["icon"] = '<span class="material-symbols-outlined">private_connectivity</span>'

        log.debug(record_dict)

        context_values = {
            "title": alter_record.get_record_title(record_dict),
            "record": record_dict,
            "record_json": record_json,
            "record_sections": record_sections,
            "record_sections_json": record_sections_json,
        }

        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/record.html", context)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)


async def get_record_view_json(request: Request):
    try:
        record: RecordsIdGet = await api.record_read(request)

        record_dict = record.to_dict()
        record_json = json.dumps(record_dict, indent=4, ensure_ascii=False)
        return PlainTextResponse(record_json)

    except Exception as e:
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)
