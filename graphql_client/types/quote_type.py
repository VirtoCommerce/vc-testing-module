from pydantic import BaseModel


class QuoteType(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.quote_attachment_type import QuoteAttachmentType
        from datetime import datetime
        from graphql_client.types.quote_shipment_method_type import QuoteShipmentMethodType
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.quote_address_type import QuoteAddressType
        from graphql_client.types.quote_item_type import QuoteItemType
        from graphql_client.types.quote_tax_detail_type import QuoteTaxDetailType
        from graphql_client.types.quote_totals_type import QuoteTotalsType

        self.cancelledDate: datetime | None
        self.cancelReason: str | None
        self.channelId: str | None
        self.comment: str | None
        self.coupon: str | None
        self.customerId: str | None
        self.customerName: str | None
        self.createdBy: str | None
        self.createdDate: datetime
        self.employeeId: str | None
        self.employeeName: str | None
        self.enableNotification: bool
        self.expirationDate: datetime | None
        self.id: str
        self.innerComment: str | None
        self.isAnonymous: bool
        self.isCancelled: bool
        self.isLocked: bool
        self.languageCode: str | None
        self.modifiedBy: str | None
        self.modifiedDate: datetime | None
        self.number: str
        self.objectType: str | None
        self.organizationId: str | None
        self.organizationName: str | None
        self.reminderDate: datetime | None
        self.status: str | None
        self.storeId: str
        self.tag: str | None
        self.currency: CurrencyType
        self.manualRelDiscountAmount: MoneyType
        self.manualShippingTotal: MoneyType
        self.manualSubTotal: MoneyType
        self.totals: QuoteTotalsType
        self.items: list[QuoteItemType]
        self.addresses: list[QuoteAddressType]
        self.attachments: list[QuoteAttachmentType]
        self.shipmentMethod: QuoteShipmentMethodType | None
        self.taxDetails: list[QuoteTaxDetailType]
        self.dynamicProperties: list[DynamicPropertyValueType]
