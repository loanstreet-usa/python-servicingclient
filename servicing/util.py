from datetime import date
from functools import wraps
from typing import Any, Callable, TypeVar, Generic, Union
from uuid import UUID

from .errors import ServicingInvalidPathParamError


T = TypeVar("T")


def is_uuid(value: Any):
    if isinstance(value, UUID):
        return True
    else:
        try:
            UUID(value)
            return True
        except (TypeError, ValueError):
            return False


class RequireUuid(Generic[T]):
    def __init__(self, kwarg: str):
        self.kwarg = kwarg

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            if not is_uuid(kwargs[self.kwarg]):
                raise ServicingInvalidPathParamError
            return func(*args, **kwargs)

        return wrapped_f


def format_date(d: Union[date, str]) -> str:
    return d.isoformat() if isinstance(d, date) else d
