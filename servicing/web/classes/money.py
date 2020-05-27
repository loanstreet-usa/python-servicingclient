from dataclasses import dataclass
from typing import Optional

from . import JsonObject, JsonValidator


@dataclass
class Money(JsonObject):
    attributes = {"amount", "currency"}

    def __init__(self, amount: str, currency: Optional[str] = "USD"):
        self.amount = amount
        self.currency = currency

    @JsonValidator("money amount is required")
    def amount_present(self):
        return self.amount is not None
