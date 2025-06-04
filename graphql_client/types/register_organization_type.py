from pydantic import BaseModel


class RegisterOrganizationType(BaseModel):
    def __init__(self):
        from graphql_client.types.member_address_type import MemberAddressType
        from graphql_client.types.member_address_type import MemberAddressType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType

        self.id: str
        self.name: str
        self.description: str | None
        self.address: MemberAddressType | None
        self.addresses: list[MemberAddressType] | None
        self.phoneNumber: str | None
        self.status: str | None
        self.createdBy: str | None
        self.ownerId: str | None
        self.dynamicProperties: list[DynamicPropertyValueType] | None
