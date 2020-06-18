from . import JsonObject, JsonValidator
from .money import Money


class Forgiveness(JsonObject):
    attributes = {"date", "amount"}

    def __init__(self, *, date: str, amount: Money):
        self.amount = amount
        self.date = date

    @JsonValidator("date is required")
    def date_present(self):
        return self.date is not None

    @JsonValidator("amount is required")
    def amount_present(self):
        return self.amount is not None
