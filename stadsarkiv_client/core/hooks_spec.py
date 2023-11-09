"""
Default hooks specification.
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log

log = get_log()


class HooksSpec:
    def __init__(self, request: Request):
        self.request = request

    def before_get_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        return context

    def after_get_record(self, record: dict, meta_data: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        return record, meta_data

    def before_api_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def after_api_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

    async def after_get_resource(self, type: str, json: dict) -> dict:
        """
        Alter the json returned from the proxies api.
        """
        return json
