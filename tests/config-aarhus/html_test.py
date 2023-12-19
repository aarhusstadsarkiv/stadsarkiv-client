"""
Test of some resources and records
"""

from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest
from bs4 import BeautifulSoup

log = get_log()


class TestHTML(unittest.TestCase):
    def test_sejrs_sedler(self):
        client = TestClient(app)
        response = client.get("/records/000110411")

        soup = BeautifulSoup(response.content, "html.parser")

        # check if there is div with the class "record-sejrs-sedler"
        record_sejrs_sedler = soup.find("div", {"class": "record-sejrs-sedler"})
        self.assertIsNotNone(record_sejrs_sedler)
