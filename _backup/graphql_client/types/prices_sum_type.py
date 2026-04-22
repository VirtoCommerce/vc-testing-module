from pydantic import BaseModel


class PricesSumType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.total: MoneyType
        self.discountTotal: MoneyType
