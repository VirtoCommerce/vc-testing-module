from pydantic import BaseModel


class TaxDetailType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.amount: MoneyType
        self.price: MoneyType
        self.rate: MoneyType
        self.name: str | None
