from pydantic import BaseModel


class ConfigurationLineItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.product import Product
        from graphql_client.types.currency_type import CurrencyType

        self.id: str | None
        self.quantity: int | None
        self.product: Product | None
        self.currency: CurrencyType
        self.listPrice: MoneyType
        self.extendedPrice: MoneyType
        self.salePrice: MoneyType
        self.discountAmount: MoneyType
