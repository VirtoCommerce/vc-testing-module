from pydantic import BaseModel


class DiscountType(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.money_type import MoneyType

        self.coupon: str | None
        self.description: str | None
        self.promotionId: str | None
        self.amount: Decimal
        self.moneyAmount: MoneyType
        self.amountWithTax: Decimal
        self.moneyAmountWithTax: MoneyType
