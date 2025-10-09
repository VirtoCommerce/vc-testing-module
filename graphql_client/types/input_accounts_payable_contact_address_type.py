from pydantic import BaseModel


class InputAccountsPayableContactAddressType(BaseModel):
    def __init__(self):

        self.city: str
        self.countryCode: str
        self.countryName: str | None
        self.email: str | None
        self.firstName: str | None
        self.key: str | None
        self.lastName: str | None
        self.line1: str
        self.line2: str | None
        self.middleName: str | None
        self.name: str | None
        self.organization: str | None
        self.phone: str | None
        self.postalCode: str
        self.regionId: str | None
        self.regionName: str | None
        self.zip: str | None
        self.outerId: str | None
        self.description: str | None
        self.addressType: int | None
