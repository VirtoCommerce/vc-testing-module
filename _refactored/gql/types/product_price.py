from .base import GqlModel
from .money import Money


class ProductPrice(GqlModel):
    list: Money
    actual: Money
