from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection


log = get_log()


class Hooks(HooksSpec):
    def before_template(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        return context

    def before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    def after_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        return query_params

    def after_record(self, record: dict) -> dict:
        """
        Alter the record dictionary after the api call
        """
        if is_collection(record, 1):

            meta_title = f"[{record['summary'][:60]} ... ]"
            record["meta_title"] = meta_title
            record["record_type"] = "sejrs_sedler"

        if is_curator(record, 4):
            if record.get("summary"):
                title = record["summary"]
                record["title"] = f"[{title}]"
                record["meta_title"] = f"[{title}"

        return record
