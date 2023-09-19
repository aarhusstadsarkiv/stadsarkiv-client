from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection


log = get_log()


class Hooks(HooksSpec):
    def alter_context(self, context: dict) -> None:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        pass

    def alter_query_params_before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    def alter_query_params_after_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        return query_params

    def alter_record(self, record_dict: dict) -> None:
        """
        Alter the record dictionary. Before the record is returned to the template.
        """
        if is_collection(record_dict, 1):

            meta_title = f"[{record_dict['summary'][:60]} ... ]"
            record_dict["meta_title"] = meta_title
            record_dict["record_type"] = "sejrs_sedler"

        if is_curator(record_dict, 4):
            if record_dict.get("summary"):
                title = record_dict["summary"]
                record_dict["title"] = f"[{title}]"
                record_dict["meta_title"] = f"[{title}"

    def get_record_title(self, title: str, record_dict: dict) -> str:
        """
        Alter the record title. Before the title is returned to the template.
        """
        return title

    # def get_record_meta_title(self, meta_title: str, record_dict: dict) -> str:

    #     if is_collection(record_dict, 1):
    #         if record_dict.get("summary"):
    #             meta_title = f"[{record_dict['summary'][:60]} ... ]"

    #     meta_title = f"{meta_title} | AarhusArkivet"
    #     return meta_title
