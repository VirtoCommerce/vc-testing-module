from gql.types.base import GqlModel
from gql.types.pickup_address import PickupAddress


class ProductPickupLocation(GqlModel):
    id: str
    is_active: bool
    name: str
    description: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    working_hours: str | None = None
    delivery_days: int | None = None
    storage_days: int | None = None
    geo_location: str | None = None
    address: PickupAddress | None = None
    availability_type: str | None = None
    availability_note: str | None = None
    available_quantity: int | None = None
