from stadsarkiv_client.facets import FACETS
from stadsarkiv_client.core import query


class NormalizeSearchFacets:

    async def __init__(self, request):
        self.facests = FACETS
        self.q = await query.get_search_query(request)
        self.query_params = await query.get_params_as_tuple_list(request, remove_keys=["q"])
        self.query_str = await query.get_params_as_query_str(request)

    def alter_search_facets(self, data):
        """Transform search facets from this format:

        {
            'availability': {'buckets': [{'value': '2', 'count': 1}]}
        }

        to this format:

        {
            "availability": {
                "2": {
                    "value": "2",
                    "count": 1
                }
            }
        }
        """

        altered_search_facets = {}
        for key, value in data.items():
            transformed_buckets = {bucket["value"]: bucket for bucket in value["buckets"]}
            altered_search_facets[key] = transformed_buckets

        return altered_search_facets


    def alter_facets_content(self, top_level_key, facets_content, facets_search, query_params):
        """Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params."""
        for facet in facets_content:
            if "children" in facet:
                alter_facets_content(top_level_key, facet["children"], facets_search, query_params)

            try:
                facet["count"] = facets_search[top_level_key][facet["id"]]["count"]
            except KeyError:
                facet["count"] = False

            # check if the facet is checked, meaning it exist in the query_params
            search = (top_level_key, facet["id"])
            if search in query_params:
                facet["checked"] = True
            else:
                facet["checked"] = False