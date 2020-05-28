from typing import Optional

from . import JsonObject, JsonValidator


class Money(JsonObject):
    attributes = {"amount", "currency"}

    def __init__(self, amount: str, currency: Optional[str] = "USD"):
        self.amount = amount
        self.currency = currency

    @JsonValidator("amount is required")
    def amount_present(self):
        return self.amount is not None

    @JsonValidator("currency is required")
    def currency_present(self):
        return self.currency is not None
