from pydantic import BaseModel


class CatalogDiscountType(BaseModel):
    def __init__(self):
        from graphql_client.types.promotion import Promotion
        from decimal import Decimal
        from graphql_client.types.money_type import MoneyType

        self.coupon: str | None
        self.description: str | None
        self.promotionId: str | None
        self.amount: Decimal
        self.moneyAmount: MoneyType
        self.amountWithTax: Decimal
        self.moneyAmountWithTax: MoneyType
        self.promotion: Promotion | None
