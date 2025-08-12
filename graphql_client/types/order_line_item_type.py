from pydantic import BaseModel


class OrderLineItemType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from decimal import Decimal
        from graphql_client.types.product import Product
        from graphql_client.types.order_discount_type import OrderDiscountType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.order_tax_detail_type import OrderTaxDetailType
        from graphql_client.types.order_configuration_item_type import OrderConfigurationItemType
        from graphql_client.types.currency_type import CurrencyType

        self.id: str
        self.productType: str | None
        self.name: str
        self.comment: str | None
        self.imageUrl: str | None
        self.isGift: bool | None
        self.shippingMethodCode: str | None
        self.fulfillmentLocationCode: str | None
        self.fulfillmentCenterId: str | None
        self.fulfillmentCenterName: str | None
        self.outerId: str | None
        self.productOuterId: str | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.measureUnit: str | None
        self.height: Decimal | None
        self.length: Decimal | None
        self.width: Decimal | None
        self.isCancelled: bool
        self.cancelledDate: datetime | None
        self.cancelReason: str | None
        self.objectType: str
        self.status: str | None
        self.statusDisplayValue: str | None
        self.categoryId: str | None
        self.catalogId: str
        self.sku: str
        self.priceId: str | None
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.listTotal: MoneyType
        self.listTotalWithTax: MoneyType
        self.taxType: str | None
        self.taxPercentRate: Decimal
        self.reserveQuantity: int
        self.quantity: int
        self.productId: str
        self.currency: CurrencyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.extendedPrice: MoneyType
        self.extendedPriceWithTax: MoneyType
        self.showPlacedPrice: bool
        self.placedPrice: MoneyType
        self.placedPriceWithTax: MoneyType
        self.taxTotal: MoneyType
        self.taxDetails: list[OrderTaxDetailType]
        self.discounts: list[OrderDiscountType]
        self.product: Product | None
        self.vendor: CommonVendor | None
        self.dynamicProperties: list[DynamicPropertyValueType]
        self.configurationItems: list[OrderConfigurationItemType] | None
