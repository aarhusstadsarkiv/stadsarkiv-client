# import requests
import json
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
# from starlette.requests import Request
from .api_base import APIBase, APIException
log = get_log()


class APIEntity(APIBase):

    async def post_entity(self, url, data: dict = {}):
        response = self.jwt_post_json(url=url, data=data)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise APIException(
                translate("Failed to create entity"), response.status_code, response.text)
