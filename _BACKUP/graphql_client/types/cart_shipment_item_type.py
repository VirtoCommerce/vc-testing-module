from pydantic import BaseModel


class CartShipmentItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.line_item_type import LineItemType

        self.quantity: int
        self.lineItem: LineItemType | None
