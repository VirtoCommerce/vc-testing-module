from pydantic import BaseModel


class OrderDiscountType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.amount: MoneyType
        self.coupon: str | None
        self.promotionId: str | None
        self.promotionName: str | None
        self.promotionDescription: str | None
        self.description: str | None
