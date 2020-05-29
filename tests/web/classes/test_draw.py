import unittest
from servicing.web.classes.draw import Draw
from servicing.web.classes.money import Money


class DrawTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            Draw(date="2020-01-01", amount=Money("10000")
                 ).to_dict(),
            {
                "amount": {
                    "amount": "10000",
                    "currency": "USD"
                },
                "date": "2020-01-01"
            }
        )
