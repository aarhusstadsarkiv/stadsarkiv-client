from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec


log = get_log()


def _is_teater_arkiv(record_dict: dict):

    # try and get first list item in curators
    try:
        curator = record_dict["curators"][0]
    except KeyError:
        return False

    if curator["id"] == 4:
        return True

    return False


class Hooks(HooksSpec):
    def alter_context(self, context: dict) -> None:
        pass
        # context["title"] = context["title"] + " [modified by plugin]"

    def alter_search_query(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    def alter_query_params_before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    def alter_query_params_after_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        return query_params

    # def get_record_title(self, title: str, record_dict: dict) -> str:
    #     return title
    #
    # curator
    def get_record_title(self, title: str, record_dict: dict) -> str:
        """
        Alter the record title. Before the title is returned to the template.
        """

        if _is_teater_arkiv(record_dict):
            summary = record_dict.get("summary", "")
            return summary

        # log.debug("title", title)

        return title

    def get_record_meta_title(self, title: str) -> str:
        title = f"{title} | AarhusArkivet"
        return title
