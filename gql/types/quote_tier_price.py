from .base import GqlModel
from .money import Money


class QuoteTierPrice(GqlModel):
    quantity: int
    price: Money
