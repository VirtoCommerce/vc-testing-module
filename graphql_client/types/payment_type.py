from pydantic import BaseModel


class PaymentType(BaseModel):
    def __init__(self):
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.discount_type import DiscountType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from decimal import Decimal
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.cart_address_type import CartAddressType

        self.id: str
        self.outerId: str | None
        self.paymentGatewayCode: str | None
        self.purpose: str | None
        self.currency: CurrencyType
        self.amount: MoneyType
        self.billingAddress: CartAddressType | None
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.total: MoneyType
        self.totalWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.taxTotal: MoneyType
        self.taxPercentRate: Decimal
        self.taxType: str | None
        self.taxDetails: list[TaxDetailType]
        self.discounts: list[DiscountType]
        self.comment: str | None
        self.vendor: CommonVendor | None
        self.dynamicProperties: list[DynamicPropertyValueType]
