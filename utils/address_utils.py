import uuid
from typing import Any

from gql.types import MemberAddress

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


def make_address(
    *,
    key_prefix: str,
    city: str = "Test City",
    country_code: str = "USA",
    country_name: str = "United States of America",
    region_id: str = "NY",
    region_name: str = "New York",
    line1: str = "1 Test Street",
    postal_code: str = "10001",
    first_name: str = "John",
    last_name: str = "Doe",
    description: str | None = None,
) -> MemberAddress:
    """Build a uniquely identifiable MemberAddress for seeding.

    A unique *key* is required so the backend does not dedupe addresses with
    similar content within a single ``updateMemberAddresses`` call — when
    *key* is omitted, the server derives one from content and collapses
    near-duplicates.

    The backend also dedupes by content (excluding key/description) across a
    single payload, so we splice the unique suffix into ``line1`` whenever
    the caller didn't already provide a uniquely valued ``line1``.
    """
    unique = uuid.uuid4().hex[:8]
    if "{unique}" in line1 or unique in line1:
        unique_line1 = line1.replace("{unique}", unique)
    else:
        unique_line1 = f"{line1} #{unique}"
    return MemberAddress(
        key=f"{key_prefix}-{unique}",
        first_name=first_name,
        last_name=last_name,
        line1=unique_line1,
        city=city,
        country_code=country_code,
        country_name=country_name,
        postal_code=postal_code,
        region_id=region_id,
        region_name=region_name,
        phone="+1 (555) 000-0000",
        email="john.doe@test.com",
        address_type=3,
        description=description or f"{key_prefix}-{unique}",
    )
