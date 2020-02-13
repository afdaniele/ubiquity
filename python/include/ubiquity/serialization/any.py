from typing import Any


def serialize_any(value: Any) -> Any:
    if isinstance(value, (int, float, bool, str)):
        return value

