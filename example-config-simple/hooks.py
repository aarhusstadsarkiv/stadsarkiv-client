from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection


log = get_log()


class Hooks(HooksSpec):
    def before_template(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | SimpleConfig"

        return context

    def before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        return query_params

    def after_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params

    def after_record(self, record: dict) -> dict:
        """
        Alter the record dictionary after the api call
        """
        if is_collection(record, 1):
            meta_title = f"[{record['summary'][:60]} ... ]"
            record["meta_title"] = meta_title
            record["record_type"] = "sejrs_sedler"
            record["representation_text"] = record["summary"]
            del record["summary"]

        if is_curator(record, 4):
            if record.get("summary"):
                title = record["summary"]
                record["title"] = f"[{title}]"
                record["meta_title"] = f"[{title}]"

        return record

    async def after_get_resource(self, type: str, json: dict) -> dict:
        """
        Alter the entity json is returned from the proxies api.
        """
        return json
