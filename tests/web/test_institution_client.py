import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import LoanClient, InstitutionClient
from servicing.web.classes.enums import TransactionType, ViewType


class InstitutionClientTests(unittest.TestCase):
    def test_list_loans(self):
        institution_id = uuid4()

        api_call = Mock()
        InstitutionClient(api_call).list_loans(institution_id=institution_id)
        self.assertTrue(api_call.called)

        _, kwargs = api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/institution/{institution_id}/loan")
        self.assertEqual(kwargs["query_params"], {"view": ViewType.BASIC.value})
