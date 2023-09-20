"""
Default hooks specification.
"""


class HooksSpec:
    def before_template(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        return context

    def after_record(self, record: dict) -> dict:
        """
        Alter the record dictionary after the api call
        """
        return record

    def before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        """
        return query_params

    def after_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        """
        return query_params
