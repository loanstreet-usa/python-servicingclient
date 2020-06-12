import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import TransactionClient
from servicing.web.classes.enums import TransactionType, ViewType


class LoanClientTests(unittest.TestCase):
    def setUp(self):
        self.base_client = Mock()
        self.transaction_client = TransactionClient(client=self.base_client)

    def test_get(self):
        transaction_id = uuid4()

        self.transaction_client.get(transaction_id=transaction_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/transaction/{transaction_id}")

    def test_void(self):
        transaction_id = uuid4()

        self.transaction_client.void(transaction_id=transaction_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/transaction/{transaction_id}/void")
