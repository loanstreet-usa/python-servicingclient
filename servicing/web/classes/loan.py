from uuid import UUID
from typing import Optional

from ...util import is_uuid
from . import JsonObject, JsonValidator
from .enums import (
    BenchmarkName,
    Compounding,
    DayCount,
    FixedPaymentType,
    Frequency,
    StartType,
)
from .money import Money


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

    @JsonValidator("amount is required")
    def amount_present(self):
        return self.amount is not None

    @JsonValidator("type is required")
    def type_present(self):
        return self.type is not None


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


class Loan(JsonObject):
    attributes = {
        "agent_id",
        "borrower_id",
        "lender_id",
        "annual_rate",
        "benchmark",
        "commitment",
        "compounding",
        "day_count",
        "fixed_payment",
        "is_revolver",
        "max_num_draws",
        "origination_date",
        "periods",
        "time_zone_id",
    }

    def __init__(
        self,
        *,
        agent_id: UUID,
        borrower_id: UUID,
        lender_id: UUID,
        annual_rate: float,
        benchmark: Optional[BenchmarkName] = None,
        commitment: Money,
        compounding: Compounding,
        day_count: DayCount,
        fixed_payment: FixedPayment,
        is_revolver: Optional[bool] = False,
        max_num_draws: Optional[int] = None,
        origination_date: str,
        periods: Periods,
        time_zone_id: str
    ):
        self.agent_id = agent_id
        self.borrower_id = borrower_id
        self.lender_id = lender_id
        self.annual_rate = str(annual_rate)
        self.benchmark = benchmark.value if benchmark else None
        self.commitment = commitment
        self.compounding = compounding.value
        self.day_count = day_count.value
        self.fixed_payment = fixed_payment
        self.is_revolver = is_revolver
        self.max_num_draws = max_num_draws
        self.origination_date = origination_date
        self.periods = periods
        self.time_zone_id = time_zone_id

    @JsonValidator("agent_id attribute is not a valid UUID")
    def agent_id_is_uuid(self):
        return is_uuid(self.agent_id)

    @JsonValidator("borrower_id attribute is not a valid UUID")
    def borrower_id_is_uuid(self):
        return is_uuid(self.borrower_id)

    @JsonValidator("lender_id attribute is not a valid UUID")
    def lender_id_is_uuid(self):
        return is_uuid(self.lender_id)

    @JsonValidator("commitment attribute is required")
    def commitment_present(self):
        return self.commitment is not None

    @JsonValidator("compounding attribute is required")
    def compounding_present(self):
        return self.compounding is not None

    @JsonValidator("day_count attribute is required")
    def day_count_present(self):
        return self.day_count is not None

    @JsonValidator("origination_date attribute is required")
    def origination_date_present(self):
        return self.origination_date is not None

    @JsonValidator("periods attribute is required")
    def periods_present(self):
        return self.periods is not None

    @JsonValidator("time_zone_id attribute is required")
    def time_zone_id_present(self):
        return self.time_zone_id is not None
