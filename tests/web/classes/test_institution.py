import unittest
from servicing.web.classes.institution import Address, Institution


class InstitutionTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            Institution(
                name="LoanStreet, Inc.",
                ticker="LOA-STR",
                address=Address(
                    street_one="29 W 30th St",
                    street_two="8th Floor",
                    city="New York",
                    state="NY",
                    zip="10001"
                )
            ).to_dict(),
            {
                "name": "LoanStreet, Inc.",
                "ticker": "LOA-STR",
                "address": {
                    "street_one": "29 W 30th St",
                    "street_two": "8th Floor",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001"
                }
            }
        )
