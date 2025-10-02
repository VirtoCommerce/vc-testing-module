from pydantic import BaseModel


class InputCreateOrganizationType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType
        from graphql_client.types.input_member_address_type import InputMemberAddressType

        self.name: str | None
        self.addresses: list[InputMemberAddressType] | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
