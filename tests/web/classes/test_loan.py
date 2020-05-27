import unittest
from servicing.web.classes.loan import Loan
from servicing.web.classes.money import Money
from servicing.web.classes.fixed_payment import FixedPayment
from servicing.web.classes.periods import Periods

from servicing.web.classes.enums import BenchmarkName, Compounding, DayCount, Frequency


class LoanTests(unittest.TestCase):
    def test_json(self):
        fixed_payment = FixedPayment(amount=Money("10000"))
        periods = Periods(count=120, frequency=Frequency.MONTHLY)
        self.assertDictEqual(
            Loan(agent_id="foo", borrower_id="bar", lender_id="baz", annual_rate=0.0475,
                 benchmark=BenchmarkName.LIBOR_OVERNIGHT, commitment=Money("1000000"),
                 compounding=Compounding.SIMPLE, day_count=DayCount.ACTUAL_360, fixed_payment=fixed_payment,
                 origination_date="2020-05-27", time_zone_id="EST", periods=periods).to_dict(),
            {
                "agent_id": "foo",
                "annual_rate": "0.0475",
                "benchmark": "LIBOR_OVERNIGHT",
                "borrower_id": "bar",
                "commitment": {
                    "amount": "1000000",
                    "currency": "USD"
                },
                "compounding": "SIMPLE",
                "day_count": "ACTUAL_360",
                "fixed_payment": {
                    "amount": {
                        "amount": "10000",
                        "currency": "USD"
                    },
                    "type": "TOTAL"
                },
                "is_revolver": False,
                "lender_id": "baz",
                "origination_date": "2020-05-27",
                "periods": {
                    "count": 120,
                    "frequency": "MONTHLY",
                    "count_deferred": 0,
                    "count_interest_only": 0,
                    "start_type": "DISBURSEMENT_DATE"
                },
                "time_zone_id": "EST"
            }
        )
