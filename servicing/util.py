from typing import Any
from uuid import UUID


def is_uuid(value: Any):
    if isinstance(value, UUID):
        return True
    else:
        try:
            UUID(value)
            return True
        except (TypeError, ValueError):
            return False
