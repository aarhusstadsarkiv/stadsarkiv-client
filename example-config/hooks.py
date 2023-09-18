from stadsarkiv_client.core.logging import get_log


log = get_log()


class Hooks:
    def alter_context(self, context: dict) -> None:
        context["title"] = context["title"] + " [modified by plugin]"

    def alter_search_query(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        return query_params

    def get_record_meta_title(self, title: str) -> str:
        title = f"{title} | AarhusArkivet"
        return title
