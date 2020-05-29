import unittest
from uuid import UUID

from servicing.web.classes.loan import Loan, FixedPayment, Periods
from servicing.web.classes.draw import Draw
from servicing.web.classes.payment import Payment

from servicing.web.classes.money import Money

from servicing.web.classes.enums import BenchmarkName, Compounding, DayCount, Frequency

from servicing.web.classes.institution import Institution
from servicing import ServicingClient


class ServicingClientTests(unittest.TestCase):
    BASE_URL = "https://api-dev.loan-street.com:8443/"

    def register_loan(self) -> UUID:
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
        return UUID(resp["loan_id"])

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

    def test_get_loan(self):
        client = ServicingClient(base_url=self.BASE_URL)
        loan_id = self.register_loan()
        resp = client.get_loan(loan_id=loan_id)
        self.assertIsNotNone(resp["loan_id"])
        self.assertEqual(str(loan_id), resp["loan_id"])

    def test_get_loan_balance(self):
        client = ServicingClient(base_url=self.BASE_URL)
        loan_id = self.register_loan()
        resp = client.get_loan_balance(loan_id=loan_id)
        self.assertIsNotNone(resp["principal"])

    def test_get_loan_interest(self):
        client = ServicingClient(base_url=self.BASE_URL)
        loan_id = self.register_loan()
        resp = client.get_loan_interest(loan_id=loan_id, start_date="2020-05-27", end_date="2020-05-27")
        self.assertTrue(isinstance(resp.data, list))

    def test_draw_funds(self):
        client = ServicingClient(base_url=self.BASE_URL)
        loan_id = self.register_loan()
        draw = Draw(amount=Money("10000"), date="2020-05-28")
        resp = client.draw_funds(loan_id=loan_id, draw=draw)
        self.assertIsNotNone(resp["transaction_id"])
        return loan_id

    def test_create_payment(self):
        client = ServicingClient(base_url=self.BASE_URL)
        loan_id = self.register_loan()
        payment = Payment(amount=Money("5000"), date="2020-05-28")
        resp = client.create_payment(loan_id=loan_id, payment=payment)
        self.assertIsNotNone(resp["transaction_id"])
        return loan_id

    def test_next_business_day(self):
        client = ServicingClient(base_url=self.BASE_URL)
        resp = client.next_business_day(date="2020-01-01")
        self.assertIsNotNone(resp["date"])
        self.assertEqual("2020-01-02", resp["date"])

    def test_previous_business_day(self):
        client = ServicingClient(base_url=self.BASE_URL)
        resp = client.previous_business_day(date="2020-01-02")
        self.assertIsNotNone(resp["date"])
        self.assertEqual("2020-01-02", resp["date"], )

    def test_get_benchmark_rate(self):
        client = ServicingClient(base_url=self.BASE_URL)
        resp = client.get_benchmark_rate(benchmark_name=BenchmarkName.PRIME, date="2020-01-01")
        self.assertIsNotNone(resp["rate"])
        self.assertEqual(BenchmarkName.PRIME.value, resp["name"])
        self.assertEqual("2020-01-01", resp["date"])
