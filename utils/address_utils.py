from typing import Any

_FIELDS_TO_COMPARE = (
    "country_code",
    "country_name",
    "region_id",
    "region_name",
    "city",
    "line1",
    "line2",
)


def addresses_equal(a: Any, b: Any) -> bool:
    return all(getattr(a, f) == getattr(b, f) for f in _FIELDS_TO_COMPARE if hasattr(a, f) and hasattr(b, f))
