from pydantic import BaseModel


class OpusContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_member_address_type import OpusMemberAddressType
        from graphql_client.types.user_type import UserType
        from datetime import datetime
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.seo_info import SeoInfo
        from graphql_client.types.opus_member_address_connection import OpusMemberAddressConnection
        from graphql_client.types.opus_contact_type import OpusContactType
        from graphql_client.types.opus_organization_connection import OpusOrganizationConnection

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
        self.defaultBillingAddress: OpusMemberAddressType | None
        self.defaultShippingAddress: OpusMemberAddressType | None
        self.addresses: OpusMemberAddressConnection | None
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
        self.organizations: OpusOrganizationConnection | None
        self.relevanceScore: float | None
        self.favoriteSupplierOuterIds: list[str]
        self.orderApproverId: str | None
        self.orderApprover: OpusContactType | None
        self.selectedShippingLocation: str | None
        self.jobTitle: str | None
        self.shippingAddresses: OpusMemberAddressConnection | None
        self.billingAddresses: OpusMemberAddressConnection | None
