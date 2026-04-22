from pydantic import BaseModel


class OrderTaxDetailType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.rate: MoneyType
        self.amount: MoneyType
        self.name: str
