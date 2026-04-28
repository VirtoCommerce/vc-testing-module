from gql.types.base import GqlModel
from gql.types.line_item import LineItem


class Wishlist(GqlModel):
    id: str
    name: str
    store_id: str
    customer_id: str
    items_count: int
    items: list[LineItem] | None = None
