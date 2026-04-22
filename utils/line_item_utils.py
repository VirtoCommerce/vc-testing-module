from gql.types.line_item import LineItem


def has_line_item(items: list[LineItem], product_id: str, quantity: int | None = None) -> bool:
    item = next((i for i in items if i.product_id == product_id), None)
    if item is None:
        return False
    if quantity is not None:
        return item.quantity == quantity
    return True
