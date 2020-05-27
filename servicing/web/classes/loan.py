from uuid import UUID
from . import JsonObject, JsonValidator


class Loan(JsonObject):
    attributes = {"agent_id", "borrower_id", "lender_id"}

    def __init__(self, *, agent_id: UUID, borrower_id: UUID, lender_id: UUID):
        self.agent_id = agent_id
        self.borrower_id = borrower_id
        self.lender_id = lender_id

    @JsonValidator("agent_id attribute is required")
    def agent_id_present(self):
        return self.agent_id is not None

    @JsonValidator("borrower_id attribute is required")
    def borrower_id_present(self):
        return self.borrower_id is not None

    @JsonValidator("lender_id attribute is required")
    def lender_id_present(self):
        return self.lender_id is not None
