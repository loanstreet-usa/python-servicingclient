from .base_client import BaseClient
from .classes.enums import BenchmarkName, TransactionType
from .classes.institution import Institution
from .classes.loan import Loan
from .classes.draw import Draw
from .classes.fund import Fund
from .classes.payment import Payment
from .classes.user import User
from .servicing_response import ServicingResponse
from uuid import UUID
from ..util import is_uuid
from ..errors import ServicingInvalidPathParamError


class ServicingClient(BaseClient):
    def status(self) -> ServicingResponse:
        return self.api_call(method="GET", path="/v1/public/status")

    def get_acl(self, oid: UUID):
        if not is_uuid(oid):
            raise ServicingInvalidPathParamError
        return self.api_call(method="GET", path=f"/v1/private/acl{oid}")

    def login(self, *, email: str, password: str) -> ServicingResponse:
        return self.api_call(
            method="POST",
            path="/v1/public/token",
            data={"email": email, "password": password},
        )

    def register_institution(self, *, institution: Institution) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/institution", data=institution.to_dict()
        )

    def get_institution(self, *, institution_id: UUID) -> ServicingResponse:
        if not is_uuid(institution_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET", path=f"/v1/private/institution/{institution_id}"
        )

    def get_institutions(self):
        return self.api_call(method="GET", path="/v1/private/institution")

    def register_loan(self, *, loan: Loan) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/loan", data=loan.to_dict()
        )

    def get_loan(self, *, loan_id: UUID) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(method="GET", path=f"/v1/private/loan/{loan_id}")

    def get_loan_balance(self, *, loan_id: UUID) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(method="GET", path=f"/v1/private/loan/{loan_id}/balance")

    def get_loan_interest(
        self, *, loan_id: UUID, start_date: str, end_date: str
    ) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        query_params = dict()
        query_params["startDate"] = start_date
        query_params["endDate"] = end_date

        return self.api_call(
            method="GET",
            path=f"/v1/private/loan/{loan_id}/interest",
            query_params=query_params,
        )

    def get_loan_invoice(self, *, loan_id: UUID, period_number: int):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET", path=f"/v1/private/loan/{loan_id}/invoice/{period_number}"
        )

    def get_loan_transactions(
        self, *, loan_id: UUID, transaction_type: TransactionType
    ):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        query_params = {"type": transaction_type.value}
        return self.api_call(
            method="GET",
            path=f"/v1/private/loan/{loan_id}/transaction",
            query_params=query_params,
        )

    def void_loan_transaction(self, *, loan_id: UUID, transaction_id: UUID):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        if not is_uuid(transaction_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST",
            path=f"/v1/private/loan/{loan_id}/transaction/{transaction_id}/void",
        )

    def get_loan_transaction(self, *, loan_id: UUID, transaction_id: UUID):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        if not is_uuid(transaction_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET",
            path=f"/v1/private/loan/{loan_id}/transaction/{transaction_id}",
        )

    def get_users(self):
        return self.api_call(method="GET", path="/v1/private/user")

    def create_user(self, *, user: User):
        return self.api_call(
            method="POST", path="/v1/private/user", data=user.to_dict()
        )

    def get_user(self, *, user_id: UUID):
        if not is_uuid(user_id):
            raise ServicingInvalidPathParamError
        return self.api_call(method="POST", path=f"/v1/private/user/{user_id}")

    def create_payment(self, *, loan_id: UUID, payment: Payment) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST",
            path=f"/v1/private/loan/{loan_id}/payment",
            data=payment.to_dict(),
        )

    def draw_funds(self, *, loan_id: UUID, draw: Draw) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST", path=f"/v1/private/loan/{loan_id}/draw", data=draw.to_dict()
        )

    def get_benchmark_rate(
        self, *, benchmark_name: BenchmarkName, date: str
    ) -> ServicingResponse:
        return self.api_call(
            method="GET", path=f"/v1/public/benchmark/{benchmark_name.value}/{date}"
        )

    def next_business_day(self, *, date: str) -> ServicingResponse:
        return self.api_call(
            method="GET", path=f"/v1/public/finance/next-business-day/{date}"
        )

    def previous_business_day(self, *, date: str) -> ServicingResponse:
        return self.api_call(
            method="GET", path=f"/v1/public/finance/previous-business-day/{date}"
        )

    def create_fund(self, *, institution_id: UUID, fund: Fund) -> ServicingResponse:
        if not is_uuid(institution_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST",
            path=f"/v1/private/institution/{institution_id}/fund",
            data=fund.to_dict(),
        )

    def get_fund(self, *, fund_id: UUID) -> ServicingResponse:
        if not is_uuid(fund_id):
            raise ServicingInvalidPathParamError
        return self.api_call(method="GET", path=f"/v1/private/fund/{fund_id}")
