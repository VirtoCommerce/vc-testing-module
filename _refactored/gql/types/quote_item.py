from .base import GqlModel
from .money import Money
from .quote_tier_price import QuoteTierPrice


class QuoteItem(GqlModel):
    id: str
    name: str
    sku: str | None = None
    product_id: str | None = None
    quantity: int
    list_price: Money
    sale_price: Money
    proposal_prices: list[QuoteTierPrice] = []
