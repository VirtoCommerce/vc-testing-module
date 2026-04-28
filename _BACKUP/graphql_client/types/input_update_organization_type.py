from pydantic import BaseModel


class InputUpdateOrganizationType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_member_address_type import InputMemberAddressType
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.id: str
        self.name: str | None
        self.memberType: str | None
        self.addresses: list[InputMemberAddressType] | None
        self.phones: list[str] | None
        self.emails: list[str] | None
        self.groups: list[str] | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
