from stadsarkiv_client.core.logging import get_log


log = get_log()


class Hooks:
    def alter_context(self, context: dict) -> None:
        context["title"] = context["title"] + " [modified by plugin]"

    def alter_search_query(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        # log.debug("alter_search_query")
        # log.debug(query_params)
        # iterate list of dicts and remove any "curector" that is not equal to: ("curator", "4")

        # query_params = [(key, value) for key, value in query_params if key != "curator" or value != "4"]
        # remove any "curator" element from list of tuples
        query_params = [(key, value) for key, value in query_params if key != "curator"]

        # add ("curator", "4") to list of tuples
        query_params.append(("curators", "4"))

        log.debug(query_params)
        return query_params
        # pass

    def get_record_title(self, title: str) -> str:
        title = f"{title} | AarhusArkivet"
        return title
