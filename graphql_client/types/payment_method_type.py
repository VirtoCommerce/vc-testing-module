from pydantic import BaseModel


class PaymentMethodType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from decimal import Decimal
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.currency_type import CurrencyType

        self.code: str
        self.description: str | None
        self.logoUrl: str | None
        self.priority: int
        self.isAvailableForPartial: bool
        self.allowCartPayment: bool
        self.name: str | None
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
        self.taxDetails: list[TaxDetailType] | None
        self.paymentMethodType: str
        self.paymentMethodGroupType: str
