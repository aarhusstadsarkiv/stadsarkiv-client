from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import os
import unittest

log = get_log()

test_user = os.getenv("TEST_USER", "")
test_password = os.getenv("TEST_PASSWORD", "")


class TestAuth(unittest.TestCase):
    def test_home(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        client = TestClient(app)
        response = client.get("/not_found")
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        client = TestClient(app)
        response = client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_post_correct(self):
        client = TestClient(app)
        response = client.post("/auth/post-login-jwt", data={"username": test_user, "password": test_password})
        self.assertEqual(response.status_code, 200)

    def test_login_post_incorrect(self):
        client = TestClient(app)
        client.follow_redirects = False
        response = client.post("/auth/post-login-jwt", data={"username": "bad.mail@test.com", "password": "bad_password"})
        # not logged in. Redirect to login
        self.assertEqual(response.status_code, 302)

    def test_post_logout(self):
        client = TestClient(app)
        client.follow_redirects = False
        response = client.post("/auth/post-logout")
        # not logged in. Redirect to login
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        client = TestClient(app)
        client.follow_redirects = False
        response = client.get("/auth/logout")
        # not logged in. Redirect to login
        self.assertEqual(response.status_code, 302)

    def test_me(self):
        client = TestClient(app)
        response = client.post("/auth/post-login-jwt", data={"username": test_user, "password": test_password})
        self.assertEqual(response.status_code, 200)

        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 200)
