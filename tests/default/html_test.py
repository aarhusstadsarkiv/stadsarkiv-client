"""
Test of some resources and records
"""

from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest
from bs4 import BeautifulSoup

log = get_log()


class TestPages(unittest.TestCase):
    def test_collections(self):
        client = TestClient(app)
        response = client.get("/collections/2")
        soup = BeautifulSoup(response.content, "html.parser")

        # check the response html and test if it contains a "div" with the class "slideshow-container"
        slideshow_container = soup.find("div", {"class": "slideshow-container"})
        self.assertIsNotNone(slideshow_container)

        # check the response html and test if it contains a "h3" with the text "Arkivserier"
        h3Arkiv = soup.find("h3", string="Arkivserier")
        self.assertIsNotNone(h3Arkiv)

        # check the response html and test if it contains a "h3" with the text "Samlingstags"
        h3Tags = soup.find("h3", string="Samlingstags")
        self.assertIsNotNone(h3Tags)

    def test_sejrs_sedler(self):
        client = TestClient(app)
        response = client.get("/records/000110411")

        soup = BeautifulSoup(response.content, "html.parser")

        # check if there is div with the class "record-sejrs-sedler"
        record_sejrs_sedler = soup.find("div", {"class": "record-sejrs-sedler"})
        self.assertIsNotNone(record_sejrs_sedler)
