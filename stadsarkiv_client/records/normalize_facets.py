from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.facets import FACETS
from stadsarkiv_client.facets import QUERY_PARAMS
from urllib.parse import quote_plus


log = get_log()


def _str_to_date(date: str):
    """convert date string to date string with correct format
    e.g. 20221231 to 2022-12-31
    """
    if not date:
        return None

    if len(date) == 8:
        return f"{date[:4]}-{date[4:6]}-{date[6:]}"

    return date


class NormalizeFacets:
    def __init__(self, request: Request, records, query_params=[], query_str=""):
        self.request = request
        self.records = records
        self.facets_search = self._get_facets_search(records["facets"])
        self.query_params = query_params
        self.query_str = query_str
        self.facets_checked: list = []
        self.FACETS = FACETS

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

    def _transform_facets(self, top_level_key, facets_content, path=None):
        if path is None:
            path = [self.FACETS[top_level_key]["label"]]

        for facet in facets_content:

            current_path = path + [facet["label"]]
            facet["path"] = current_path

            if "children" in facet:
                self._transform_facets(top_level_key, facet["children"], current_path)

            try:
                facet_count = self.facets_search[top_level_key][facet["id"]]["count"]
            except KeyError:
                facet_count = 0

            facet["count"] = facet_count

            search = (top_level_key, facet["id"])
            if search in self.query_params:
                facet["checked"] = True

                # Generate a facet_checked dict (used as search filter)
                facet_checked = {}
                facet_checked["checked_label"] = " > ".join(current_path)
                facet_checked["query_name"] = top_level_key
                facet_checked["query_value"] = facet["id"]
                facet_checked["reverse_query"] = self.query_str.replace(
                    f"{top_level_key}={facet['id']}&", f"-{top_level_key}={facet['id']}&"
                )
                facet_checked["remove_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", "")
                facet_checked["checked"] = True
                facet_checked["search_query"] = self.query_str
                facet_checked["count"] = facet_count
                self.facets_checked.append(facet_checked)

            else:

                facet["count"] = facet_count
                facet["checked"] = False
                facet["search_query"] = self.query_str + f"{top_level_key}={facet['id']}&"

    def _get_label(self, key, value):
        """Get the label for a facet."""
        label = QUERY_PARAMS[key]["label"]
        if key == "date_from" or key == "date_to":
            return label + " " + _str_to_date(value)

        if key == "q":
            return f"{label} '{value}'"

        return label + " " + value

    def get_checked_facets(self):
        """get a list of facets that are checked (meaning that they are working filters).
        Add a remove_query key to the facet, which is the query string without the facet.
        """
        facets_checked = self.facets_checked

        # Ignore menu facets. Then have been set in the _transform_facets method.
        ignore_keys = [key for key in FACETS.keys()]
        ignore_keys.extend(["size", "start", "sort", "direction"])
        for query_name, query_value in self.query_params:
            if query_name not in QUERY_PARAMS or query_name in ignore_keys:
                continue

            if not query_value:
                continue

            # Generate a facet_checked dict (used as search filter)
            facet_checked = {}
            checked_label = self._get_label(query_name, query_value)

            facet_checked["query_name"] = query_name
            facet_checked["query_value"] = query_value
            facet_checked["remove_query"] = self.query_str.replace(f"{query_name}={quote_plus(query_value)}&", "")
            facet_checked["checked_label"] = checked_label
            facets_checked.append(facet_checked)

        log.debug(self.query_params)

        for facet_checked in facets_checked:
            log.debug(facet_checked)

        return facets_checked

    def get_transformed_facets(self):
        """Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params."""
        for key, value in FACETS.items():
            self._transform_facets(key, value["content"])

        return self.FACETS
