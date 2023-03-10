import requests
import json
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from starlette.requests import Request
from .fastapi_base import FastAPIBase
log = get_log()


class FastAPIException(Exception):
    pass


class Schemas(FastAPIBase):

    async def get_schemas(self):

        response = self.jwt_get_json(url='/schemas')
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException(
                translate("Failed to get schemas"), response.status_code, response.text)

    async def get_schema(self, cookie: str, schema_id: str):
        pass
