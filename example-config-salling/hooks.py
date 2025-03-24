from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec


log = get_log()


class Hooks(HooksSpec):
    def __init__(self, request):
        super().__init__(request)

    async def before_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | SallingArkivet"

        return context

    async def before_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """
        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "organisations"]
        query_params.append(("organisations", "107434"))
        
        # online
        query_params.append(("availability", "4"))
        # images
        query_params.append(("content_types", "61"))


        return query_params

    async def after_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        This example removes all curators from the query params.
        This is done to avoid that the curator added in the before_search method is added to filters and search cookie.
        """
        # organisations=107434
        query_params = [(key, value) for key, value in query_params if key != "organisations"]
        
        # online
        query_params = [(key, value) for key, value in query_params if key != "availability"]
        # images
        query_params = [(key, value) for key, value in query_params if key != "content_types"]

        return query_params
