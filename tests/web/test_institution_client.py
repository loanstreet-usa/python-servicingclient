import unittest
from unittest.mock import Mock
from uuid import uuid4

from servicing.web.client import InstitutionClient
from servicing.web.classes.enums import ViewType


class InstitutionClientTests(unittest.TestCase):
    def setUp(self):
        self.base_client = Mock()
        self.institution_client = InstitutionClient(client=self.base_client)

    def test_list_loans(self):
        institution_id = uuid4()

        self.institution_client.list_loans(institution_id=institution_id)
        self.assertTrue(self.base_client.api_call.called)

        _, kwargs = self.base_client.api_call.call_args
        self.assertEqual(kwargs["path"], f"/v1/private/institution/{institution_id}/loan")
        self.assertEqual(kwargs["query_params"], {"view": ViewType.BASIC.value})
