from pydantic import BaseModel


class PickupLocationType(BaseModel):
    def __init__(self):
        from graphql_client.types.pickup_address_type import PickupAddressType

        self.id: str
        self.isActive: bool
        self.name: str
        self.description: str | None
        self.contactEmail: str | None
        self.contactPhone: str | None
        self.workingHours: str | None
        self.geoLocation: str | None
        self.address: PickupAddressType | None
