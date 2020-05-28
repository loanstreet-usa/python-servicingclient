import unittest
from uuid import UUID

from servicing.web.classes.loan import Loan, FixedPayment, Periods
from servicing.web.classes.money import Money
from servicing.web.classes.enums import BenchmarkName, Compounding, DayCount, Frequency


class LoanTests(unittest.TestCase):
    def test_json(self):
        agent_id = UUID("cac761d1-9666-4c8e-8128-f3227b9ef6fe")
        borrower_id = UUID("01bf113e-4648-4859-8a2a-42bebb411a83")
        lender_id = UUID("b5ba849f-6975-4e90-b2e4-fbdec3514a68")
        fixed_payment = FixedPayment(amount=Money("10000"))
        periods = Periods(count=120, frequency=Frequency.MONTHLY)
        self.assertDictEqual(
            Loan(agent_id=agent_id, borrower_id=borrower_id, lender_id=lender_id, annual_rate=0.0475,
                 benchmark=BenchmarkName.LIBOR_OVERNIGHT, commitment=Money("1000000"),
                 compounding=Compounding.SIMPLE, day_count=DayCount.ACTUAL_360, fixed_payment=fixed_payment,
                 origination_date="2020-05-27", time_zone_id="America/New_York", periods=periods).to_dict(),
            {
                "agent_id": agent_id,
                "annual_rate": "0.0475",
                "benchmark": "LIBOR_OVERNIGHT",
                "borrower_id": borrower_id,
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
                "lender_id": lender_id,
                "origination_date": "2020-05-27",
                "periods": {
                    "count": 120,
                    "frequency": "MONTHLY",
                    "count_deferred": 0,
                    "count_interest_only": 0,
                    "start_type": "DISBURSEMENT_DATE"
                },
                "time_zone_id": "America/New_York"
            }
        )
