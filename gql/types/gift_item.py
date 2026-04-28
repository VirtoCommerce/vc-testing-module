from .base import GqlModel


class GiftItem(GqlModel):
    id: str
    quantity: int
    product_id: str | None = None
    name: str
    line_item_id: str | None = None
