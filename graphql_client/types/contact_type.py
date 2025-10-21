from pydantic import BaseModel


class ContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.seo_info import SeoInfo
        from graphql_client.types.member_address_type import MemberAddressType
        from graphql_client.types.organization_connection import OrganizationConnection
        from datetime import datetime
        from graphql_client.types.user_type import UserType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.member_address_connection import MemberAddressConnection

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
        self.firstName: str
        self.lastName: str
        self.middleName: str | None
        self.fullName: str
        self.about: str
        self.defaultLanguage: str | None
        self.currencyCode: str | None
        self.birthDate: datetime | None
        self.securityAccounts: list[UserType] | None
        self.organizationId: str | None
        self.selectedAddressId: str | None
        self.organizationsIds: list[str]
        self.organizations: OrganizationConnection | None
