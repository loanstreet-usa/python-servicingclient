import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import LoanClient


class LoanClientTests(unittest.TestCase):
    def setUp(self):
        self.base_client = Mock()
        self.loan_client = LoanClient(client=self.base_client)

    def test_list_transactions(self):
        loan_id = uuid4()

        self.loan_client.list_transactions(loan_id=loan_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}/transaction")
