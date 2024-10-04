"""
Default hooks specification.
query_params is a list of tuples. Example: [("collection", 1), ("series", 2)]
"""

from starlette.requests import Request
from starlette.responses import Response
from stadsarkiv_client.core.logging import get_log
import contextlib

log = get_log()


class HooksSpec:
    def __init__(self, request: Request):
        self.request = request

    def after_routes_init(self, routes: list) -> list:
        """
        Alter the routes after the base routes have been initialized.
        You may add or remove routes here.
        """
        return routes

    async def before_response(self, response: Response) -> Response:
        """
        Alter the response before it is returned.
        """
        return response

    async def after_login_success(self, response: dict) -> dict:
        """
        Alter the response after a successful login.
        """
        return response

    async def after_login_failure(self, response: dict) -> dict:
        """
        Alter the response after a login failure
        """
        return response

    async def before_get_auto_complete(self, query_params: list) -> list:
        """
        Alter the query params before the autocomplete is executed.
        """
        query_params.append(("limit", "25"))  # default limit
        return query_params

    async def after_get_auto_complete(self, query_params: list) -> list:
        """
        Alter the query params after the autocomplete is executed.
        """
        return query_params

    async def before_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned, e.g. to the template.
        """
        return context

    async def after_get_record(self, record: dict, meta_data: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        return record, meta_data

    async def after_get_record_and_types(self, record: dict, record_and_types: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        return record, record_and_types

    async def before_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    async def after_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

    async def after_get_resource(self, type: str, resource: dict) -> dict:
        """
        Alter the json returned from the proxies api.
        """
        return resource

    @staticmethod
    @contextlib.asynccontextmanager
    async def lifespan(app):

        try:
            log.info("App lifecycle started")
            yield
        finally:
            log.info("App lifecycle ended")
