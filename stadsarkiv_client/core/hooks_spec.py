"""
Default hooks specification.
"""

from stadsarkiv_client.core.logging import get_log

log = get_log()


class HooksSpec:
    def before_template(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        return context

    def after_record(self, record: dict) -> dict:
        """
        Alter the record dictionary after the api call
        """
        return record

    def before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def after_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

    async def after_get_resource(self, type: str, json: dict) -> dict:
        """
        Alter the json returned from the proxies api.
        """
        return json
