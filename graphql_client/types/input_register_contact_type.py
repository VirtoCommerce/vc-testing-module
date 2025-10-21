from pydantic import BaseModel


class InputRegisterContactType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.input_member_address_type import InputMemberAddressType
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.firstName: str
        self.lastName: str
        self.middleName: str | None
        self.phoneNumber: str | None
        self.birthdate: datetime | None
        self.address: InputMemberAddressType | None
        self.about: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
