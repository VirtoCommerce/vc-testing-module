from pydantic import BaseModel


class ConfigurationLineItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.product import Product
        from graphql_client.types.currency_type import CurrencyType

        self.id: str | None
        self.text: str | None
        self.quantity: int
        self.product: Product | None
        self.currency: CurrencyType | None
        self.listPrice: MoneyType | None
        self.extendedPrice: MoneyType | None
        self.salePrice: MoneyType | None
        self.discountAmount: MoneyType | None
