from pydantic import BaseModel


class LoyaltyBalanceResult(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.currentBalance: Decimal
        self.resultBalance: Decimal
