from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection


log = get_log()


class Hooks(HooksSpec):
    def __init__(self, request):
        super().__init__(request)

    async def before_get_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | AarhusArkivet"

        return context

    async def before_api_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        return query_params

    async def after_api_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

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

    async def after_get_resource(self, type: str, json: dict) -> dict:
        """
        Alter the entity json is returned from the proxies api.
        """
        return json
