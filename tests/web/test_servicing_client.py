import asyncio
import re
import unittest

import servicing.errors as err
from servicing import ServicingClient
from tests.web.mock_servicing_api_server import setup_mock_servicing_api_server, cleanup_mock_servicing_api_server


class ServicingClientTests(unittest.TestCase):

    def setUp(self):
        setup_mock_servicing_api_server(self)

        self.client = ServicingClient(
            token="1234",
            base_url="http://localhost:8888",
        )

    def tearDown(self):
        cleanup_mock_servicing_api_server(self)

    pattern_for_language = re.compile("python/(\\S+)", re.IGNORECASE)
    pattern_for_package_identifier = re.compile("servicingclient/(\\S+)")

    def test_api_calls_return_a_response(self):
        self.client.token = "status"
        resp = self.client.status()
        self.assertTrue(resp["status"] == "OK")

    def test_api_calls_include_user_agent(self):
        self.client.token = "status"
        resp = self.client.status()
        self.assertEqual(200, resp.status)

    def test_login(self):
        resp = self.client.login(email="support@loan-street.com", password="not-a-valid-password")
        self.assertEqual(200, resp.status)
        self.assertGreater(len(resp['token']), 0)
