from .base_client import BaseClient
from .classes.institution import Institution
from .classes.loan import Loan
from .classes.draw import Draw
from .classes.payment import Payment
from .servicing_response import ServicingResponse
from uuid import UUID
from ..util import is_uuid
from ..errors import ServicingInvalidPathParamError


class ServicingClient(BaseClient):
    def status(self) -> ServicingResponse:
        return self.api_call(method="GET", path="/v1/public/status")

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

    def register_loan(self, *, loan: Loan) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/loan", data=loan.to_dict()
        )

    def draw_funds(self, *, loan_id: UUID, draw: Draw):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError

        return self.api_call(
            method="POST", path=f"/v1/private/loan/{loan_id}/draw", data=draw.to_dict()
        )

    def create_payment(self, *, loan_id: UUID, payment: Payment):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError

        return self.api_call(
            method="POST",
            path=f"/v1/private/loan/{loan_id}/payment",
            data=payment.to_dict(),
        )

    def next_business_day(self, *, date: str):
        return self.api_call(
            method="GET", path=f"/v1/public/finance/next-business-day/{date}"
        )

    def previous_business_day(self, *, date: str):
        return self.api_call(
            method="GET", path=f"/v1/public/finance/previous-business-day/{date}"
        )
