from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection
import typing

log = get_log()


class Hooks(HooksSpec):

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
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | SimpleConfig"

        return context

    async def after_get_record(self, record: dict, meta_data: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        if is_collection(record, 1):
            meta_title = f"[{record['summary'][:60]} ... ]"
            meta_data["meta_title"] = meta_title
            meta_data["record_type"] = "sejrs_sedler"

            meta_data["representation_text"] = record["summary"]
            del record["summary"]

        if is_curator(record, 4):
            if record.get("summary"):
                title = record["summary"]
                meta_data["title"] = f"[{title}]"
                meta_data["meta_title"] = f"[{title}]"

        return record, meta_data

    async def after_get_record_and_types(self, record: dict, record_and_types: dict) -> tuple:
        """
        Alter the record and meta_data dictionaries after the api call
        """
        return record, record_and_types

    async def before_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """
        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    async def after_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        This example removes all curators from the query params.
        This is done to avoid that the curator added in the before_search method is added to filters and search cookie.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]

        return query_params

    async def after_get_resource(self, type: str, resource: dict) -> dict:
        """
        Alter the json returned from the proxies api.
        """
        return resource

    async def before_resource_response(self, response: typing.Any) -> typing.Any:
        """
        Before the reponse is returned to the template.
        This is a good place to alter the response before it is returned.
        E.g. you want to set a cookie or alter the response.
        """
        return response
