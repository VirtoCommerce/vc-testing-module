from gql.types.base import GqlModel
from gql.types.money import Money


class LineItem(GqlModel):
    id: str
    sku: str
    product_id: str
    name: str
    quantity: int
    list_price: Money | None = None
    sale_price: Money | None = None
    placed_price: Money | None = None
    extended_price: Money | None = None
    discount_amount: Money | None = None
    selected_for_checkout: bool = True
