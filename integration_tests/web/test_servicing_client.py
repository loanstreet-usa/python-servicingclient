import os
import ssl
import unittest
from uuid import UUID

import random

from servicing import ServicingClient
from servicing.web.classes.draw import Draw
from servicing.web.classes.enums import BenchmarkName, Compounding, DayCount, Frequency, TransactionType
from servicing.web.classes.fund import Fund
from servicing.web.classes.institution import Institution
from servicing.web.classes.loan import Loan, FixedPayment, Periods
from servicing.web.classes.money import Money
from servicing.web.classes.payment import Payment


class ServicingClientTests(unittest.TestCase):
    BASE_URL = os.getenv("BASE_URL") or "https://api-dev.loan-street.com:8443/"
    TOKEN = os.getenv("TOKEN")

    def setUp(self):
        self.client = ServicingClient(base_url=self.BASE_URL, token=self.TOKEN, ssl=self.__ssl_ctx())

    def __ssl_ctx(self):
        ctx = None

        if "localhost" in self.BASE_URL.lower() or "127.0.0.1" in self.BASE_URL:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        return ctx

    def register_loan(self) -> UUID:
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
        resp = self.client.loan.register(loan=loan).validate()
        self.assertIsNotNone(resp["loan_id"])
        return UUID(resp["loan_id"])

    def register_institution(self) -> UUID:
        institution = Institution(name="Integration Tests, Inc.")
        resp = self.client.institution.register(institution=institution).validate()
        self.assertIsNotNone(resp["institution_id"])
        return UUID(resp["institution_id"])

    def test_register_institution(self):
        institution = Institution(name="Integration Tests, Inc.")
        resp = self.client.institution.register(institution=institution).validate()
        self.assertIsNotNone(resp["institution_id"])

    def test_get_institution(self):
        institution_id = self.register_institution()
        resp = self.client.institution.get(institution_id=institution_id).validate()
        self.assertIsNotNone(resp["institution_id"])

    def test_get_institutions(self):
        resp = self.client.institution.get_all().validate()
        self.assertTrue(isinstance(resp.data, list))

    def test_register_loan(self):
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
        resp = self.client.loan.register(loan=loan).validate()
        self.assertIsNotNone(resp["loan_id"])

    def test_get_loan(self):
        loan_id = self.register_loan()
        resp = self.client.loan.get(loan_id=loan_id).validate()
        self.assertIsNotNone(resp["loan_id"])
        self.assertEqual(str(loan_id), resp["loan_id"])

    def test_update_loan(self):
        loan_id = self.register_loan()

        fixed_payment = FixedPayment(amount=Money("10000"))
        periods = Periods(count=120, frequency=Frequency.MONTHLY)
        random_rate = random.random()

        updated_loan = Loan(
            agent_id=UUID("898be40f-a26e-43cb-b15c-679afdc7e278"),
            borrower_id=UUID("d12fd58d-5939-4dc2-9d57-7c3fd7ce9026"),
            lender_id=UUID("467001e0-0631-45c0-b7f1-02b4424fd526"),
            annual_rate=random_rate,
            benchmark=BenchmarkName.LIBOR_OVERNIGHT,
            commitment=Money("1000000"),
            compounding=Compounding.SIMPLE,
            day_count=DayCount.ACTUAL_360,
            fixed_payment=fixed_payment,
            origination_date="2020-05-27",
            time_zone_id="America/New_York",
            periods=periods,
        )
        
        resp = self.client.loan.update(
            loan_id=loan_id,
            loan=updated_loan
        ).validate()

        self.assertIsNotNone(resp["loan_id"])
        self.assertEqual(str(loan_id), resp["loan_id"])
        self.assertAlmostEqual(random_rate, resp["annual_rate"])

    def test_get_loan_invoice(self):
        loan_id = self.register_loan()
        draw = Draw(amount=Money("10000"), date="2020-05-28")
        self.client.loan.draw_funds(loan_id=loan_id, draw=draw)

        resp = self.client.loan.get_invoice(loan_id=loan_id, period_number=1).validate()
        self.assertIsNotNone(resp["loan_id"])
        self.assertIsNotNone(resp["period_number"])

    def test_list_loan_transactions(self):
        loan_id = self.register_loan()
        draw = Draw(amount=Money("10000"), date="2020-05-28")
        self.client.loan.draw_funds(loan_id=loan_id, draw=draw)
        resp = self.client.loan.list_transactions(loan_id=loan_id, transaction_type=TransactionType.DRAW).validate()
        self.assertTrue(isinstance(resp.data, list))

    def test_get_loan_transaction(self):
        loan_id = self.register_loan()

        payment = Payment(amount=Money("5000"), date="2020-05-28")
        resp = self.client.loan.create_payment(loan_id=loan_id, payment=payment)
        self.assertIsNotNone(resp["transaction_id"])
        transaction_id = UUID(resp["transaction_id"])
        resp = self.client.transaction.get(transaction_id=transaction_id).validate()

        self.assertIsNotNone(resp["transaction_id"])
        self.assertIsNotNone(resp["date"])
        self.assertEqual("2020-05-28", resp["date"])

    def test_list_loan_trackers(self):
        loan_id = self.register_loan()
        resp = self.client.loan.list_trackers(loan_id=loan_id).validate()
        self.assertTrue(isinstance(resp.data, list))

    def test_draw_funds(self):
        loan_id = self.register_loan()
        draw = Draw(amount=Money("10000"), date="2020-05-28")
        resp = self.client.loan.draw_funds(loan_id=loan_id, draw=draw).validate()
        self.assertIsNotNone(resp["transaction_id"])
        return loan_id

    def test_create_payment(self):
        loan_id = self.register_loan()
        payment = Payment(amount=Money("5000"), date="2020-05-28")
        resp = self.client.loan.create_payment(loan_id=loan_id, payment=payment).validate()
        self.assertIsNotNone(resp["transaction_id"])
        return loan_id

    def test_next_business_day(self):
        resp = self.client.next_business_day(date="2020-01-01").validate()
        self.assertIsNotNone(resp["date"])
        self.assertEqual("2020-01-02", resp["date"])

    def test_previous_business_day(self):
        resp = self.client.previous_business_day(date="2020-01-02")
        self.assertIsNotNone(resp["date"])
        self.assertEqual("2020-01-02", resp["date"], )

    @unittest.skip
    def test_get_benchmark_rate(self):
        resp = self.client.get_benchmark_rate(benchmark_name=BenchmarkName.PRIME, date="2020-01-02").validate()
        self.assertIsNotNone(resp["rate"])
        self.assertEqual(BenchmarkName.PRIME.value, resp["name"])
        self.assertEqual("2020-01-01", resp["date"])

    def test_create_fund(self):
        institution_id = self.register_institution()
        fund = Fund(name="Integration Fund")
        resp = self.client.institution.create_fund(institution_id=institution_id, fund=fund).validate()
        self.assertIsNotNone(resp["fund_id"])

    def test_get_fund(self):
        institution_id = self.register_institution()
        fund = Fund(name="Integration Fund")
        resp = self.client.institution.create_fund(institution_id=institution_id, fund=fund).validate()
        self.assertIsNotNone(resp["fund_id"])
        fund_id = resp["fund_id"]
        resp = self.client.institution.get_fund(fund_id=fund_id).validate()
        self.assertIsNotNone(resp["fund_id"])
        self.assertEqual(fund_id, resp["fund_id"])
        self.assertEqual(str(institution_id), resp["institution_id"])
        self.assertEqual(fund.name, resp["name"])

    def test_get_users(self):
        resp = self.client.user.get_all().validate()
        self.assertTrue(isinstance(resp.data, list))
