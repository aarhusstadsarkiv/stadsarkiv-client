"""
Default hooks specification.
"""


class HooksSpec:
    def alter_context(self, context: dict) -> None:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        pass

    def alter_record(self, record_dict: dict) -> None:
        """
        Alter the record just recieved from the api.
        """
        pass

    def alter_query_params_before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def alter_query_params_after_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def get_record_title(self, title: str, record_dict: dict) -> str:
        """
        Alter the record title. Before the title is returned to the template.
        """
        return title

    def get_record_meta_title(self, title: str, record_dict: dict) -> str:
        """
        Alter the html title tag for a record page.
        """
        return title
