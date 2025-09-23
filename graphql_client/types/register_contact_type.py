from pydantic import BaseModel


class RegisterContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.member_address_type import MemberAddressType
        from datetime import datetime
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType

        self.id: str
        self.firstName: str
        self.lastName: str
        self.middleName: str | None
        self.phoneNumber: str | None
        self.birthdate: datetime | None
        self.status: str | None
        self.createdBy: str | None
        self.about: str | None
        self.address: MemberAddressType | None
        self.dynamicProperties: list[DynamicPropertyValueType] | None
