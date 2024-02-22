from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api
from stadsarkiv_client.core.relations import format_relations, sort_data


log = get_log()


async def post(request: Request):
    try:
        await api.proxies_post_relations(request)
        return JSONResponse({"error": False, "message": "Relation er oprettet"})

    except OpenAwsException as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": e.message})

    except Exception as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": "Internal Server Error"})


async def get(request: Request):
    type = request.path_params.get("type", "")
    id = request.path_params.get("id", "")
    try:
        relations = await api.proxies_get_relations(request, type, id)
        relations_formatted = format_relations(type, relations)
        if type == "people":
            relations_formatted = sort_data(relations_formatted, "display_label")
        if type == "events":
            relations_formatted = sort_data(relations_formatted, "rel_label")
        return JSONResponse(relations_formatted)

    except OpenAwsException as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": e.message})

    except Exception as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": "Internal Server Error"})
