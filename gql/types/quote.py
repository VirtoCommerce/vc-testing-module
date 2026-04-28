from .base import GqlModel
from .quote_item import QuoteItem
from .quote_totals import QuoteTotals


class Quote(GqlModel):
    id: str
    number: str
    status: str | None = None
    store_id: str
    customer_id: str | None = None
    comment: str | None = None
    is_anonymous: bool
    is_cancelled: bool
    totals: QuoteTotals
    items: list[QuoteItem] = []
