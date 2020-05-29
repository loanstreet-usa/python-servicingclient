from .base_client import BaseClient
from .classes.institution import Institution
from .classes.loan import Loan
from .classes.draw import Draw
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

    def draw_fund(self, *, loan_id: UUID, draw: Draw):
        if not is_uuid(loan_id):
            raise ServicingInvalidPathParamError

        return self.api_call(
            method="POST", path=f"/v1/private/loan/{loan_id}/draw", data=draw.to_dict()
        )
