from uuid import UUID
from typing import Optional
from . import JsonObject, JsonValidator
from .enums import BenchmarkName, Compounding, DayCount
from .money import Money
from .fixed_payment import FixedPayment
from .periods import Periods


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
        self.benchmark = benchmark.value
        self.commitment = commitment
        self.compounding = compounding.value
        self.day_count = day_count.value
        self.fixed_payment = fixed_payment
        self.is_revolver = is_revolver
        self.max_num_draws = max_num_draws
        self.origination_date = origination_date
        self.periods = periods
        self.time_zone_id = time_zone_id


@JsonValidator("agent_id attribute is required")
def agent_id_present(self):
    return self.agent_id is not None


@JsonValidator("borrower_id attribute is required")
def borrower_id_present(self):
    return self.borrower_id is not None


@JsonValidator("lender_id attribute is required")
def lender_id_present(self):
    return self.lender_id is not None


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
