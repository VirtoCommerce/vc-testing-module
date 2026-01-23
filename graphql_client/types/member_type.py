from pydantic import BaseModel


class MemberType(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.member_address_type import MemberAddressType
        from graphql_client.types.member_address_connection import MemberAddressConnection
        from graphql_client.types.seo_info import SeoInfo

        self.id: str
        self.outerId: str | None
        self.memberType: str
        self.name: str | None
        self.status: str | None
        self.phones: list[str]
        self.emails: list[str]
        self.groups: list[str]
        self.seoObjectType: str
        self.seoInfo: SeoInfo | None
        self.defaultBillingAddress: MemberAddressType | None
        self.defaultShippingAddress: MemberAddressType | None
        self.addresses: MemberAddressConnection | None
        self.dynamicProperties: list[DynamicPropertyValueType]
