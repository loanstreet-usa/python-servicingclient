import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import LoanClient
from servicing.web.classes.enums import TrackerType, ViewType


class LoanClientTests(unittest.TestCase):
    def setUp(self):
        self.base_client = Mock()
        self.loan_client = LoanClient(client=self.base_client)

    def test_get(self):
        loan_id = uuid4()

        self.loan_client.get(loan_id=loan_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}")

    def test_get_detailed_view(self):
        loan_id = uuid4()

        self.loan_client.get(loan_id=loan_id, view=ViewType.DETAILED)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["query_params"], {"view": "DETAILED"})

    def test_list_transactions(self):
        loan_id = uuid4()

        self.loan_client.list_transactions(loan_id=loan_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}/transaction")

    def test_list_trackers(self):
        loan_id = uuid4()

        self.loan_client.list_trackers(loan_id=loan_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/loan/{loan_id}/tracker")

    def test_list_trackers_with_end_date(self):
        loan_id = uuid4()

        self.loan_client.list_trackers(loan_id=loan_id, end_date="2020-01-01")
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["query_params"], {"end_date": "2020-01-01"})

    def test_list_trackers_with_tracker_type(self):
        loan_id = uuid4()

        self.loan_client.list_trackers(loan_id=loan_id, tracker_type=TrackerType.DAILY_INTEREST_ACCRUAL)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["query_params"], {"type": TrackerType.DAILY_INTEREST_ACCRUAL.value})
