from pydantic import BaseModel


class ShippingMethodType(BaseModel):
    def __init__(self):
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.money_type import MoneyType

        self.id: str
        self.code: str
        self.logoUrl: str | None
        self.name: str | None
        self.description: str | None
        self.optionName: str | None
        self.optionDescription: str | None
        self.priority: int
        self.currency: CurrencyType
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.total: MoneyType
        self.totalWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
