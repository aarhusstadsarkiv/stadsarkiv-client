from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.facets import FACETS
from stadsarkiv_client.facets import QUERY_PARAMS

# from stadsarkiv_client.facets import RESOURCE_TYPES
from urllib.parse import quote_plus


log = get_log()


def _str_to_date(date: str):
    """convert date string to date string with correct format
    e.g. 20221231 to 2022-12-31
    """

    if len(date) == 8:
        return f"{date[:4]}-{date[4:6]}-{date[6:]}"

    return date


def _get_records_filter(records, key) -> dict:
    """Get a single filter from records"""

    if not records.get("filters"):
        return {}

    try:
        filters = records["filters"]
        for filter in filters:
            if filter["key"] == key:
                return filter
        return {}
    except KeyError:
        return {}


class NormalizeFacets:
    def __init__(self, request: Request, records: dict, query_params: list = [], query_str: str = ""):
        self.request = request
        self.records = records
        self.facets_search = self._get_facets_search(records["facets"])
        self.query_params = query_params
        self.query_str = query_str
        self.filters = records.get("filters", [])
        self.FACETS = FACETS

        log.debug(self.filters)

    def _get_facets_search(self, data):
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

    def _transform_facets(self, top_level_key: str, facets_content: dict, path: list = []):
        if not path:
            path = [self.FACETS[top_level_key]["label"]]

        for facet in facets_content:
            current_path = path + [facet["label"]]
            facet["path"] = current_path
            facet["checked_label"] = " > ".join(current_path)

            if "children" in facet:
                self._transform_facets(top_level_key, facet["children"], current_path)

            try:
                facet["count"] = self.facets_search[top_level_key][facet["id"]]["count"]
            except KeyError:
                facet["count"] = 0

            search = (top_level_key, facet["id"])
            facet["remove_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", "")

            label = ""
            try:
                label = str(QUERY_PARAMS[top_level_key]["label"])
            except KeyError:
                pass

            full_label = f"{label} {facet['label']}"
            facet["alter_label"] = full_label
            facet["reverse_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", f"-{top_level_key}={facet['id']}&")

            if search in self.query_params:
                facet["checked"] = True
                facet["search_query"] = self.query_str
            else:
                facet["checked"] = False
                facet["search_query"] = self.query_str + f"{top_level_key}={facet['id']}&"

    def _set_facets_checked(self, top_level_key: str, facets_content: dict, facets_checked: list = []):
        for facet in facets_content:
            if "children" in facet:
                self._set_facets_checked(top_level_key, facet["children"], facets_checked)

            if facet["checked"]:
                facets_checked.append(facet)

    def _get_checked_facets_flatten(self):
        facets_checked = []

        for key, value in FACETS.items():
            self._set_facets_checked(key, value["content"], facets_checked)

        return facets_checked

    def _get_label(self, query_name: str, query_value: str):
        """
        Get the label for a facet.
        The label is found in QUERY_PARAMS:

        If the facet is a date, then part of the label is the date in a readable format.
        If the key is the search query ('q') then part of the label is the search query.

        The label is not found in QUERY_PARAMS:
        If the key is not found in QUERY_PARAMS. Then try to get the resolved filter from records.
        """
        label = str(QUERY_PARAMS[query_name]["label"])

        if query_name == "date_from" or query_name == "date_to":
            return label + " " + _str_to_date(query_value)

        if query_name == "q":
            return label + " " + query_value

        return f"{label} (Unresolved) '{query_name}'={query_value}"

    def _get_entity_link(self, key, value):
        """Get the link to entity if the entity can be displayed"""
        pass

    def get_checked_facets(self):
        """get a list of facets that are checked (meaning that they are working filters).
        Add a remove_query key to the facet, which is the query string without the facet.
        """
        facets_checked = self._get_checked_facets_flatten()
        ignore_keys = ["subjects", "content_types", "usability", "availability", "size", "start", "sort", "direction"]

        for query_name, query_value in self.query_params:
            if query_name not in QUERY_PARAMS or query_name in ignore_keys:
                continue

            # definition = QUERY_PARAMS[query_name]

            # try:
            #     label = definition.get("label")
            # except KeyError:
            #     continue
            log.debug(query_name)
            facet = {}
            facet["type"] = query_name
            facet["remove_query"] = self.query_str.replace(f"{query_name}={quote_plus(query_value)}&", "")

            checked_label = self._get_label(query_name, str(query_value))  # query_value to str in case it is an int
            facet["checked_label"] = checked_label
            facets_checked.append(facet)

        return facets_checked

    def _get_unresolved_facet(self, facet):
        pass

    def get_transformed_facets(self):
        """Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params."""
        for key, value in FACETS.items():
            self._transform_facets(key, value["content"])

        return self.FACETS
