from pydantic import BaseModel


class TierPriceType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.quantity: int
