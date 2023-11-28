"""
Normalize the tree of facets. (Right side of the search page)
Generate query parts of links that can be used to remove a facet from the search.
Add count to the facets.

Also generate a list of checked facets (search filters that are enabled).
"""

from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.core.dynamic_settings import settings_facets
from stadsarkiv_client.settings_query_params import settings_query_params
from stadsarkiv_client.core import query
from urllib.parse import quote_plus


log = get_log()


class NormalizeFacets:
    def __init__(self, request: Request, records, query_params=[], facets_resolved={}, query_str=""):
        self.request = request
        self.records = records
        self.active_facets = records["active_facets"]
        self.query_params = query_params
        self.query_str = query_str
        self.facets_resolved = facets_resolved
        self.facets_checked: list = []
        self.facets = settings_facets

        # query params without the "-" (negated) prefix
        self.query_params_cleaned = [(name.lstrip("-"), value) for name, value in self.query_params]

        # All query params that are negated
        self.query_params_negated = [(name.lstrip("-"), value) for name, value in self.query_params if name.startswith("-")]

    def _transform_facets(self, facet_name, children, tree_path_labels=None):
        """
        Alter facets tree that are display on the left side of the search page.
        """

        if tree_path_labels is None:
            tree_path_labels = [self.facets[facet_name]["label"]]

        for facet in children:
            tree_path_labels_current = tree_path_labels + [facet["label"]]

            if "children" in facet:
                self._transform_facets(facet_name, facet["children"], tree_path_labels_current)

            try:
                facet_count = self.active_facets[facet_name][facet["id"]]["count"]
            except KeyError:
                facet_count = 0

            facet["count"] = facet_count

            search = (facet_name, facet["id"])
            if search in self.query_params_cleaned:
                # Indicate on the facet that it is checked
                facet["checked"] = True

                facet_checked = {}
                facet_checked["is_negated"] = search in self.query_params_negated
                facet_checked["checked_label"] = " > ".join(tree_path_labels_current)
                facet_checked["query_name"] = facet_name
                facet_checked["query_value"] = facet["id"]
                facet_checked = self._set_facet_urls(facet_checked)
                facet_checked["count"] = facet_count
                self.facets_checked.append(facet_checked)

            else:
                facet["count"] = facet_count
                facet["checked"] = False
                facet["search_query"] = self.query_str + f"{facet_name}={facet['id']}&"

    def _get_facets_resolved_label(self, key, value):
        """
        Get the inner dict from the facets_resolved dict.
        """
        try:
            resolved = self.facets_resolved[key][value]["display_label"]
            return resolved
        except KeyError:
            return None

    def _get_filter_label(self, key, value):
        """
        Get the label for a facet.
        """
        label_settings = settings_query_params[key]["label"]
        resolved_label = self._get_facets_resolved_label(key, value)

        if resolved_label:
            return label_settings + " " + resolved_label

        if key == "date_from" or key == "date_to":
            return label_settings + " " + _str_to_date(value)

        if key == "q":
            return f"{label_settings} '{value}'"

        return label_settings + " " + value

    def _get_entity_path(self, key):
        """
        collection -> collections. All other entities correspond to the key.
        """
        try:
            return settings_query_params[key]["entity_path"]
        except KeyError:
            return key

    def _get_enitity_url(self, key, value):
        """
        Get the link for a facet.
        """
        resolved = self._get_facets_resolved_label(key, value)
        definition = settings_query_params[key]

        if resolved and not definition.get("label_only", False):
            entity_path = self._get_entity_path(key)
            return f"/{entity_path}/{value}"
        return None

    def get_filters(self):
        """
        Get filters that are set in the query params.
        """
        facets_checked = self.facets_checked

        # Ignore menu facets. They have been set in the _transform_facets method.
        ignore_keys = [key for key in settings_facets.keys()]

        # But check if settings_facets[key]["allow_facet_removal"] is True
        # if true then it it should be removed from the ignore_keys list
        for key in settings_facets.keys():
            if settings_facets[key].get("allow_facet_removal") is True:
                ignore_keys.remove(key)

        # Ignore the size, start, sort and direction query params
        ignore_keys.extend(["size", "start", "sort", "direction"])
        for query_name, query_value in self.query_params_cleaned:
            if query_name not in settings_query_params or query_name in ignore_keys:
                continue

            if not query_value:
                continue

            checked_label = self._get_filter_label(query_name, query_value)

            facet_checked = {}
            facet_checked["is_negated"] = query_name in self.query_params_negated
            facet_checked["query_name"] = query_name
            facet_checked["query_value"] = query_value
            facet_checked = self._set_facet_urls(facet_checked)
            facet_checked["checked_label"] = checked_label
            facet_checked["entity_url"] = self._get_enitity_url(query_name, query_value)
            facets_checked.append(facet_checked)

        # remove duplicates
        facets_checked = [dict(t) for t in {tuple(facet.items()) for facet in facets_checked}]

        # Sort the search filters based on the query_params order
        query_order = {(name, value): index for index, (name, value) in enumerate(self.query_params)}

        # Sort the search filters based on the query_order
        sorted_facets_checked = sorted(facets_checked, key=lambda x: query_order.get((x["query_name"], x["query_value"]), float("inf")))

        return sorted_facets_checked

    def get_transformed_facets(self):
        """
        Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params.
        """
        for key, value in settings_facets.items():
            if value["type"] == "default":
                self._transform_facets(key, value["content"])

        return self.facets

    def _set_facet_urls(self, facet_checked):
        """
        Set the remove query for a facet.
        """
        is_negated = facet_checked["is_negated"]
        query_name = facet_checked["query_name"]
        query_value = facet_checked["query_value"]

        query_negated = f"-{query_name}={quote_plus(query_value)}&"
        query_not_negated = f"{query_name}={quote_plus(query_value)}&"

        # create remove query
        if is_negated:
            facet_checked["remove_query"] = self.query_str.replace(query_negated, "")
        else:
            facet_checked["remove_query"] = self.query_str.replace(query_not_negated, "")

        # create negated query
        if is_negated:
            facet_checked["negated_query"] = self.query_str.replace(query_negated, query_not_negated)
        else:
            facet_checked["negated_query"] = self.query_str.replace(query_not_negated, query_negated)

        return facet_checked


def _str_to_date(date: str):
    """convert date string to date string with correct format
    e.g. 20221231 to 2022-12-31
    """

    return f"{date[:4]}-{date[4:6]}-{date[6:]}"
