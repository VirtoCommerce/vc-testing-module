from pydantic import BaseModel


class InputCreateContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType
        from graphql_client.types.input_member_address_type import InputMemberAddressType

        self.id: str | None
        self.name: str | None
        self.memberType: str | None
        self.addresses: list[InputMemberAddressType] | None
        self.phones: list[str] | None
        self.emails: list[str] | None
        self.groups: list[str] | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
        self.fullName: str | None
        self.firstName: str
        self.lastName: str
        self.middleName: str | None
        self.salutation: str | None
        self.photoUrl: str | None
        self.timeZone: str | None
        self.defaultLanguage: str | None
        self.currencyCode: str | None
        self.about: str | None
        self.selectedAddressId: str | None
        self.organizations: list[str] | None
