from enum import Enum


class TransactionType(Enum):
    DRAW = "DRAW"
    PAYMENT = "PAYMENT"
    SALE = "SALE"
