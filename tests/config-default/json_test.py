"""
Test of JSON response
"""

from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest
import json

log = get_log()


class TestJSON(unittest.TestCase):
    def test_collections(self):
        client = TestClient(app)
        response = client.get("/records/000309478/json/meta_data")

        # response as json
        json_response = response.json()

        json_expected = """
        
        
        
{
  "id": "000309478",
  "real_id": "309478",
  "allowed_by_ip": false,
  "title": "Aarhus Vejviser 1997",
  "meta_title": "Aarhus Vejviser 1997",
  "meta_description": "",
  "icon": {
    "icon": "description",
    "label": "Andet materiale"
  },
  "copyright_id": 7,
  "legal_id": 1,
  "contractual_id": 5,
  "availability_id": 3,
  "usability_id": 4,
  "collection_id": 204,
  "series": null,
  "content_types_label": "",
  "is_representations_online": false,
  "is_downloadable": false
}
    """
        # parse json
        json_expected = json.loads(json_expected)
        self.assertEqual(json_response, json_expected)
