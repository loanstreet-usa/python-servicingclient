from datetime import date
from typing import Optional, Union

import abc

from .base_client import BaseClient
from .classes.enums import BenchmarkName, TransactionType, ViewType
from .classes.institution import Institution
from .classes.loan import Loan
from .classes.draw import Draw
from .classes.fund import Fund
from .classes.payment import Payment
from .classes.user import User
from .servicing_response import ServicingResponse
from uuid import UUID
from ..util import is_uuid, RequireUuid, format_date
from ..errors import ServicingInvalidPathParamError


class ResourceClient(abc.ABC):
    def __init__(self, *, client: BaseClient):
        self.api_call = client.api_call


class InstitutionClient(ResourceClient):
    def register(self, *, institution: Institution) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/institution", data=institution.to_dict()
        )

    def get(self, *, institution_id: UUID) -> ServicingResponse:
        if not is_uuid(institution_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET", path=f"/v1/private/institution/{institution_id}"
        )

    def get_all(self):
        return self.api_call(method="GET", path="/v1/private/institution")

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

    def list_loans(
        self, *, institution_id: UUID, view: ViewType = ViewType.BASIC
    ) -> ServicingResponse:
        if not is_uuid(institution_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET",
            path=f"/v1/private/institution/{institution_id}/loan",
            query_params={"view": view.value},
        )


class LoanClient(ResourceClient):
    def register(self, *, loan: Loan) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/loan", data=loan.to_dict()
        )

    def get(
        self, *, loan_id: UUID, view: Optional[ViewType] = None
    ) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError

        query_params = {}

        if view is not None:
            query_params["view"] = view.value

        return self.api_call(
            method="GET", path=f"/v1/private/loan/{loan_id}", query_params=query_params
        )

    def update(self, *, loan_id: UUID, loan: Loan) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="PUT", path=f"/v1/private/loan/{loan_id}", data=loan.to_dict()
        )

    def get_invoice(self, *, loan_id: UUID, period_number: int):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="GET", path=f"/v1/private/loan/{loan_id}/invoice/{period_number}"
        )

    def list_transactions(
        self, *, loan_id: UUID, transaction_type: Optional[TransactionType] = None
    ):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError

        query_params = {}

        if transaction_type is not None:
            query_params["type"] = transaction_type.value

        return self.api_call(
            method="GET",
            path=f"/v1/private/loan/{loan_id}/transaction",
            query_params=query_params,
        )

    @RequireUuid("loan_id")
    def list_trackers(
        self, *, loan_id: UUID, end_date: Optional[Union[date, str]] = None
    ):
        query_params = {}

        if end_date is not None:
            query_params["end_date"] = format_date(end_date)

        return self.api_call(
            method="GET",
            path=f"/v1/private/loan/{loan_id}/tracker",
            query_params=query_params,
        )

    def draw_funds(self, *, loan_id: UUID, draw: Draw) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST", path=f"/v1/private/loan/{loan_id}/draw", data=draw.to_dict()
        )

    def create_payment(self, *, loan_id: UUID, payment: Payment) -> ServicingResponse:
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError
        return self.api_call(
            method="POST",
            path=f"/v1/private/loan/{loan_id}/payment",
            data=payment.to_dict(),
        )


class TransactionClient(ResourceClient):
    def get(self, *, transaction_id: UUID):
        if not is_uuid(transaction_id):
            raise ServicingInvalidPathParamError

        return self.api_call(
            method="GET", path=f"/v1/private/transaction/{transaction_id}"
        )

    def void(self, *, transaction_id: UUID):
        if not is_uuid(transaction_id):
            raise ServicingInvalidPathParamError

        return self.api_call(
            method="POST", path=f"/v1/private/transaction/{transaction_id}/void"
        )


class UserClient(ResourceClient):
    def get_all(self):
        return self.api_call(method="GET", path="/v1/private/user")

    def create(self, *, user: User):
        return self.api_call(
            method="POST", path="/v1/private/user", data=user.to_dict()
        )

    def get(self, *, user_id: UUID):
        if not is_uuid(user_id):
            raise ServicingInvalidPathParamError
        return self.api_call(method="POST", path=f"/v1/private/user/{user_id}")


class ServicingClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.institution = InstitutionClient(client=self)
        self.loan = LoanClient(client=self)
        self.user = UserClient(client=self)
        self.transaction = TransactionClient(client=self)

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
