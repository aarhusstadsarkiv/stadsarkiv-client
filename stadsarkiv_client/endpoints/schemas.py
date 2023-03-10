from starlette.requests import Request
# from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.schemas import Schemas
# from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
import json
log = get_log()


async def get_schemas(request: Request):

    schema = Schemas(request=request)
    schemas = await schema.get_schemas()

    context_values = {"title": translate("Schemas"), "schemas": json.dumps(schemas, indent=2, default=str)}
    context = get_context(request, context_values=context_values)

    return templates.TemplateResponse('schemas/schemas.html', context)
