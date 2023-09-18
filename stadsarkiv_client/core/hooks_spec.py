"""
Default hooks specification.
"""


class Hooks:
    def alter_context(self, context: dict) -> None:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        pass

    def alter_search_query(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def get_record_meta_title(self, title: str) -> str:
        """
        Alter the html title tag for a record page.
        """
        return title
