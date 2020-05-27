import unittest

from servicing.web.servicing_response import ServicingResponse


class TestServicingResponse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_servicing_response(self):
        response = ServicingResponse(
            method="GET",
            url="https://localhost:8443/v1/public/status",
            data={
                "status": "OK"
            },
            headers={},
            status=200,
        )

        self.assertTrue(response.validate() == response)
        self.assertTrue(response.status == 200)
        self.assertTrue("status" in response.data)
        self.assertTrue(response["status"] == "OK")
        self.assertTrue(response.get("status") == "OK")