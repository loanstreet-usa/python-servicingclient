import unittest

from servicing.web.classes.misc_fee import MiscFee
from servicing.web.classes.money import Money


class MiscFeeTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            MiscFee(date="2020-01-01", amount=Money("500")
                    ).to_dict(),
            {
                "amount": {
                    "amount": "500",
                    "currency": "USD"
                },
                "date": "2020-01-01"
            }
        )
