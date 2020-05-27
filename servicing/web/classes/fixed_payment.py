from typing import Optional
from . import JsonObject, JsonValidator
from .money import Money
from .enums.fixed_payment_type import FixedPaymentType


class FixedPayment(JsonObject):
    attributes = {"amount", "type"}

    def __init__(
        self,
        *,
        amount: Money,
        type: Optional[FixedPaymentType] = FixedPaymentType.TOTAL
    ):
        self.amount = amount
        self.type = type.value

    @JsonValidator("fixed payment amount is required")
    def amount_present(self):
        return self.amount is not None
