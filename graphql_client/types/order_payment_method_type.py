from pydantic import BaseModel


class OrderPaymentMethodType(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.order_tax_detail_type import OrderTaxDetailType
        from graphql_client.types.currency_type import CurrencyType

        self.code: str
        self.name: str | None
        self.description: str | None
        self.logoUrl: str | None
        self.priority: int
        self.isActive: bool
        self.isAvailableForPartial: bool
        self.typeName: str
        self.storeId: str | None
        self.currency: CurrencyType
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.total: MoneyType
        self.totalWithTax: MoneyType
        self.taxType: str | None
        self.taxPercentRate: Decimal
        self.taxTotal: MoneyType
        self.taxDetails: list[OrderTaxDetailType] | None
        self.paymentMethodType: int
        self.paymentMethodGroupType: int
