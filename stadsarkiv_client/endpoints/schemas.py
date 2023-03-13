from starlette.requests import Request
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.schemas import Schemas
from stadsarkiv_client.api_client.fastapi_base import FastAPIBase
# from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from json import JSONDecodeError
import json
log = get_log()


async def get_schemas(request: Request):

    schema = Schemas(request=request)
    schemas = await schema.get_schemas()

    context_values = {"title": translate("Schemas"), "schemas": schemas}
    log.debug(type(schemas))
    log.debug(schemas)

    for schema in schemas:
        log.debug(schema)

    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('schemas/schemas.html', context)


async def post_schema(request: Request):

    try:

        form = await request.form()
        type = str(form.get('type'))
        data = str(form.get('data'))

        data_dict = {}
        data_dict["type"] = type

        data = json.loads(data)
        data_dict["data"] = data

        schema = FastAPIBase(request=request)
        schema.jwt_post_json(url="/schemas/", json=data_dict)
        flash.set_message(request, translate("Schema created."), type="success")

    except JSONDecodeError:
        flash.set_message(request, translate("Invalid JSON in data."), type="error")
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return RedirectResponse(url='/schemas', status_code=302)
