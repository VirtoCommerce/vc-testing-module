from pydantic import BaseModel


class ProductPickupLocation(BaseModel):
    def __init__(self):
        from graphql_client.types.product_pickup_availability_type import ProductPickupAvailabilityType
        from graphql_client.types.pickup_location_address_type import PickupLocationAddressType

        self.id: str
        self.isActive: bool
        self.name: str
        self.description: str | None
        self.contactEmail: str | None
        self.contactPhone: str | None
        self.workingHours: str | None
        self.deliveryDays: int | None
        self.storageDays: int | None
        self.geoLocation: str | None
        self.address: PickupLocationAddressType | None
        self.availabilityType: ProductPickupAvailabilityType | None
        self.availabilityNote: str | None
        self.availableQuantity: int | None
