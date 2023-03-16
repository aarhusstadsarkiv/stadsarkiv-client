# import requests
import json
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log

# from starlette.requests import Request
from .api_base import APIBase, APIException

log = get_log()


class APISchema(APIBase):
    async def get_schemas(self):
        response = self.jwt_get_json(url="/schemas")
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise APIException(translate("Failed to get schemas"), response.status_code, response.text)

    async def get_schema(self, schema_type: str, as_text: bool = False):
        url = "/schemas/" + schema_type
        response = self.jwt_get_json(url=url)
        if response.status_code == 200:
            if as_text:
                return response.content

            return json.loads(response.content)
        else:
            raise APIException(translate("Failed to get schema"), response.status_code, response.text)

    async def post_schema(self, type: str):
        url = "/schema/"
        response = self.jwt_get_json(url=url)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise APIException(translate("Failed to create schema"), response.status_code, response.text)
