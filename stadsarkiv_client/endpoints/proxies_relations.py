from starlette.requests import Request
from starlette.responses import JSONResponse
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api


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


async def get(request: Request, type: str, id: str):
    try:
        result = await api.proxies_get_relations(request, type, id)
        return result

    except OpenAwsException as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": e.message})

    except Exception as e:
        log.exception(e)
        return JSONResponse({"error": True, "message": "Internal Server Error"})
