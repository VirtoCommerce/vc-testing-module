from pydantic import BaseModel


class PickupLocationAddressType(BaseModel):
    def __init__(self):

        self.id: str
        self.key: str | None
        self.name: str | None
        self.organization: str | None
        self.countryCode: str | None
        self.countryName: str | None
        self.city: str | None
        self.postalCode: str | None
        self.line1: str | None
        self.line2: str | None
        self.regionId: str | None
        self.regionName: str | None
        self.phone: str | None
        self.email: str | None
        self.outerId: str | None
        self.description: str | None
        self.addressType: int | None
