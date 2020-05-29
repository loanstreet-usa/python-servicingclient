import unittest
from servicing.web.classes.payment import Payment
from servicing.web.classes.money import Money


class PaymentTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            Payment(date="2020-01-01", amount=Money("5000")
                    ).to_dict(),
            {
                "amount": {
                    "amount": "5000",
                    "currency": "USD"
                },
                "date": "2020-01-01"
            }
        )
