import unittest
from uuid import UUID

from servicing.web.classes.loan import Loan, FixedPayment, Periods

from servicing.web.classes.money import Money

from servicing.web.classes.enums import BenchmarkName, Compounding, DayCount, Frequency

from servicing.web.classes.institution import Institution
from servicing import ServicingClient


class ServicingClientTests(unittest.TestCase):
    BASE_URL = "https://api-dev.loan-street.com:8443/"

    def test_register_institution(self):
        client = ServicingClient(base_url=self.BASE_URL)
        institution = Institution(name="Integration Tests, Inc.")
        resp = client.register_institution(institution=institution)
        self.assertIsNotNone(resp["institution_id"])

    def test_register_loan(self):
        client = ServicingClient(base_url=self.BASE_URL)
        fixed_payment = FixedPayment(amount=Money("10000"))
        periods = Periods(count=120, frequency=Frequency.MONTHLY)
        loan = Loan(
            agent_id=UUID("898be40f-a26e-43cb-b15c-679afdc7e278"),
            borrower_id=UUID("d12fd58d-5939-4dc2-9d57-7c3fd7ce9026"),
            lender_id=UUID("467001e0-0631-45c0-b7f1-02b4424fd526"),
            annual_rate=0.0475,
            benchmark=BenchmarkName.LIBOR_OVERNIGHT,
            commitment=Money("1000000"),
            compounding=Compounding.SIMPLE,
            day_count=DayCount.ACTUAL_360,
            fixed_payment=fixed_payment,
            origination_date="2020-05-27",
            time_zone_id="America/New_York",
            periods=periods,
        )
        resp = client.register_loan(loan=loan)
        self.assertIsNotNone(resp["loan_id"])
