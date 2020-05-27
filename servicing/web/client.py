from .base_client import BaseClient
from .classes.institution import Institution
from .classes.loan import Loan
from .servicing_response import ServicingResponse


class ServicingClient(BaseClient):
    def status(self) -> ServicingResponse:
        return self.api_call(method="GET", path="/v1/public/status")

    def register_institution(self, *, institution: Institution) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/institution", data=institution.to_dict()
        )

    def register_loan(self, *, loan: Loan) -> ServicingResponse:
        return self.api_call(
            method="POST", path="/v1/private/loan", data=loan.to_dict()
        )
