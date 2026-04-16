from gql.types.base import GqlModel
from gql.types.line_item import LineItem
from gql.types.money import Money
from gql.types.sharing_setting import SharingSetting


class ShoppingList(GqlModel):
    id: str
    name: str
    store_id: str | None = None
    customer_id: str | None = None
    customer_name: str | None = None
    items: list[LineItem] = []
    items_count: int | None = None
    description: str | None = None
    sub_total: Money
    sharing_setting: SharingSetting | None = None
