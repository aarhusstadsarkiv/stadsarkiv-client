from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest

log = get_log()

test_user = "dennis.iversen@gmail.com"
test_password = "testtest"

correct_login = {"username": test_user, "password": test_password}
incorrect_login = data = {"username": "bad.mail@test.com", "password": "bad_password"}

log.info(f"test_user: {test_user}")
log.info(f"test_password: {test_password}")


class TestAuth(unittest.TestCase):
    def test_home_get(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_not_found_get(self):
        client = TestClient(app)
        response = client.get("/not_found")
        self.assertEqual(response.status_code, 404)

    def test_login_get(self):
        client = TestClient(app)
        response = client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_correct_post(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/")

    def test_login_incorrect_post(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=incorrect_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/auth/login")

    def test_logout_post(self):
        client = TestClient(app)
        response = client.post("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login")

    def test_logout_get(self):
        client = TestClient(app)
        response = client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login")
        # self.assertEqual(response.status_code, 302)

    def test_me_loggedin_get(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login)  # type: ignore
        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 200)

    def test_me_not_logged_in_get(self):
        client = TestClient(app)
        response = client.get("/auth/me", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login")
