from pydantic import BaseModel


class AccountsPayableContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.core_address_type import CoreAddressType

        self.firstName: str | None
        self.lastName: str | None
        self.fullName: str
        self.email: str | None
        self.phone: str | None
        self.address: CoreAddressType | None
