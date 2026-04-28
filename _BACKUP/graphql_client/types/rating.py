from pydantic import BaseModel


class Rating(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.value: Decimal
        self.reviewCount: int
