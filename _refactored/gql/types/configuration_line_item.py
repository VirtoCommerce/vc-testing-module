from .base import GqlModel
from .money import Money
from .product import Product


class ConfigurationLineItem(GqlModel):
    id: str | None = None
    text: str | None = None
    quantity: int
    product: Product | None = None
    list_price: Money | None = None
    sale_price: Money | None = None
    extended_price: Money | None = None
    discount_amount: Money | None = None
