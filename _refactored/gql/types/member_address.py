from gql.types.base import GqlModel


class MemberAddress(GqlModel):
    id: str | None = None
    key: str | None = None
    is_default: bool = False
    is_favorite: bool = False
    city: str | None = None
    country_code: str | None = None
    country_name: str | None = None
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    line1: str | None = None
    line2: str | None = None
    name: str | None = None
    organization: str | None = None
    phone: str | None = None
    postal_code: str
    region_id: str | None = None
    region_name: str | None = None
    zip: str | None = None
    outer_id: str | None = None
    description: str | None = None
    address_type: int | None = None
