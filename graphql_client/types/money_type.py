from pydantic import BaseModel


class MoneyType(BaseModel):
    def __init__(self):
        from graphql_client.types.currency_type import CurrencyType
        from decimal import Decimal

        self.amount: Decimal
        self.currency: CurrencyType
        self.decimalDigits: int
        self.formattedAmount: str
        self.formattedAmountWithoutCurrency: str
        self.formattedAmountWithoutPoint: str
        self.formattedAmountWithoutPointAndCurrency: str
