from typing import Optional
from . import JsonObject, JsonValidator
from .enums import Frequency, StartType


class Periods(JsonObject):
    attributes = {
        "count",
        "frequency",
        "day_of_month",
        "count_deferred",
        "count_interest_only",
        "start_type",
    }

    def __init__(
        self,
        *,
        count: int,
        frequency: Frequency,
        day_of_month: Optional[int] = None,
        count_deferred: Optional[int] = 0,
        count_interest_only: Optional[int] = 0,
        start_type: Optional[StartType] = StartType.DISBURSEMENT_DATE
    ):
        self.count = count
        self.frequency = frequency.value
        self.day_of_month = day_of_month
        self.count_deferred = count_deferred
        self.count_interest_only = count_interest_only
        self.start_type = start_type.value

    @JsonValidator("count is required")
    def count_present(self):
        return self.count is not None

    @JsonValidator("frequency is required")
    def frequency_present(self):
        return self.frequency is not None
