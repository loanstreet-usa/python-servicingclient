import unittest
from servicing.web.classes.fund import Fund


class FundTests(unittest.TestCase):
    def test_json(self):
        self.assertDictEqual(
            Fund(name="Sample Fund").to_dict(),
            {
                "name": "Sample Fund"
            }
        )
