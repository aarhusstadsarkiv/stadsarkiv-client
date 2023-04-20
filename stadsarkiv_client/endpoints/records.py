from starlette.requests import Request
from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import json
from stadsarkiv_client.core.alter_records import alter_record
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
        # for sure this is a 404
        raise HTTPException(404, detail=str(e), headers=None)


async def get_records_search_results(request: Request):
    try:
        context_values = {"title": translate("Search results")}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/search.html", context)

    except Exception as e:
        # for sure this is a 404
        raise HTTPException(404, detail=str(e), headers=None)


def set_sections(record_dict: dict):

    abstract = ['collectors', 'content_types', 'creators', 'date_from', 'curators', 'id']
    description = ['heading', 'summary', 'collection', 'series_normalized', 'subjects']
    copyright = ['copyright_status']
    relations = ['organisations', 'locations']
    copyright_extra = ['contractual_status', 'other_legal_restrictions']
    availability = ['availability']
    media = ['representations']

    sections = {
        "abstract": {}, "description": {}, "copyright": {}, "relations": {},
        "copyright_extra": {}, "availability": {}, "media": {}, "other": {}
    }

    for key, value in record_dict.items():
        if key in abstract:
            sections['abstract'][key] = value
        elif key in description:
            sections['description'][key] = value
        elif key in copyright:
            sections['copyright'][key] = value
        elif key in relations:
            sections['relations'][key] = value
        elif key in copyright_extra:
            sections['copyright_extra'][key] = value
        elif key in availability:
            sections['availability'] = record_dict[key]
        elif key in media:
            sections['media'][key] = value
        else:
            sections['other'][key] = value

    return sections


async def get_record_view(request: Request):
    try:
        record: RecordsIdGet = await api.record_read(request)
        record_dict = record.to_dict()
        record_dict = alter_record(record_dict)
        record_sections = set_sections(record_dict)
        record_sections_json = json.dumps(record_sections, indent=4, ensure_ascii=False)
        context_values = {
            "title": translate("Entity"),
            "record_sections": record_sections,
            "record_sections_json": record_sections_json,
        }

        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse("records/record.html", context)

    except Exception as e:
        # for sure this is a 404
        log.exception(e)
        raise HTTPException(404, detail=str(e), headers=None)
