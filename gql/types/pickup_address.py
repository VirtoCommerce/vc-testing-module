from gql.types.base import GqlModel


class PickupAddress(GqlModel):
    id: str
    key: str | None = None
    name: str | None = None
    organization: str | None = None
    country_code: str | None = None
    country_name: str | None = None
    city: str | None = None
    postal_code: str | None = None
    line1: str | None = None
    line2: str | None = None
    region_id: str | None = None
    region_name: str | None = None
    phone: str | None = None
    email: str | None = None
    outer_id: str | None = None
    description: str | None = None
    address_type: int | None = None
