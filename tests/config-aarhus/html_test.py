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
    def test_representations_sejrs_sedler(self):
        client = TestClient(app)
        response = client.get("/records/000110411")

        soup = BeautifulSoup(response.content, "html.parser")

        # check if there is div with the class "record-sejrs-sedler"
        elem = soup.find("div", {"class": "record-sejrs-sedler"})
        self.assertIsNotNone(elem)

    def test_representations_image(self):
        client = TestClient(app)
        response = client.get("/records/000186239")

        soup = BeautifulSoup(response.content, "html.parser")

        # check if there is div with the class "record-sejrs-sedler"
        overlays = soup.find("div", {"class": "overlays"})
        self.assertIsNotNone(overlays)

        # check if id = "overlay-image" exists
        elem = soup.find("div", {"class": "overlay-wrapper"})
        self.assertIsNotNone(elem)

        elem = soup.find("div", {"class": "overlay-actions"})
        self.assertIsNotNone(elem)

    def test_representations_audio(self):
        client = TestClient(app)
        response = client.get("/records/000466996")

        soup = BeautifulSoup(response.content, "html.parser")

        elem = soup.find("audio")
        self.assertIsNotNone(elem)

    def test_representations_video(self):
        client = TestClient(app)
        response = client.get("/records/000313141")

        soup = BeautifulSoup(response.content, "html.parser")

        elem = soup.find("video")
        self.assertIsNotNone(elem)

    def test_representations_slideshow(self):
        client = TestClient(app)
        response = client.get("/collections/1")

        soup = BeautifulSoup(response.content, "html.parser")

        elem = soup.find("div", {"class": "slideshow-container"})
        self.assertIsNotNone(elem)


if __name__ == "__main__":
    unittest.main()
