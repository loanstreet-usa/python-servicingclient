import unittest
from servicing.web.classes.loan import Loan


class LoanTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            Loan(agent_id="foo", borrower_id="bar", lender_id="baz").to_dict(),
            {
                "agent_id": "foo",
                "borrower_id": "bar",
                "lender_id": "baz"
            }
        )
