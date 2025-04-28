from pydantic import BaseModel


class QuoteAddressType(BaseModel):
    def __init__(self):

        self.addressType: int | None
        self.id: str | None
        self.key: str | None
        self.outerId: str | None
        self.name: str | None
        self.countryCode: str | None
        self.countryName: str
        self.postalCode: str | None
        self.regionId: str | None
        self.regionName: str | None
        self.city: str
        self.line1: str | None
        self.line2: str | None
        self.email: str | None
        self.phone: str | None
        self.firstName: str
        self.lastName: str
        self.organization: str | None
