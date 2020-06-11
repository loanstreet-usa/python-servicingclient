import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import LoanClient
from servicing.web.classes.enums import TransactionType, ViewType


class LoanClientTests(unittest.TestCase):
    def test_get_transactions(self):
        loan_id = uuid4()

        api_call = Mock()
        LoanClient(api_call).get_transactions(loan_id=loan_id)
        self.assertTrue(api_call.called)

        _, kwargs = api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}/transaction")
        self.assertEqual(kwargs["query_params"], {"view": ViewType.BASIC.value})

    def test_get_transactions_with_transaction_type(self):
        loan_id = uuid4()

        api_call = Mock()
        LoanClient(api_call).get_transactions(loan_id=loan_id, transaction_type=TransactionType.DRAW)
        self.assertTrue(api_call.called)

        _, kwargs = api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}/transaction")
        self.assertEqual(kwargs["query_params"], {"type": TransactionType.DRAW.value, "view": ViewType.BASIC.value})