from pydantic import BaseModel


class QuoteTierPriceType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.quantity: int
        self.price: MoneyType
