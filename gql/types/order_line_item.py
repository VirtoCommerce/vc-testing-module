from .base import GqlModel
from .money import Money


class OrderLineItem(GqlModel):
    id: str
    name: str
    sku: str
    product_id: str
    quantity: int
    price: Money
    extended_price: Money
