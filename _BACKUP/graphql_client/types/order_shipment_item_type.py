from pydantic import BaseModel


class OrderShipmentItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.order_line_item_type import OrderLineItemType

        self.id: str
        self.lineItemId: str | None
        self.lineItem: OrderLineItemType | None
        self.barCode: str | None
        self.quantity: int
        self.outerId: str | None
        self.status: str | None
