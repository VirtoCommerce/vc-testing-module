from pydantic import BaseModel


class OpusSupplierOrderShipmentItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.order_line_item_type import OrderLineItemType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.supplier_type import SupplierType

        self.price: MoneyType
        self.updatedPrice: MoneyType | None
        self.supplier: SupplierType
        self.lineItem: OrderLineItemType
        self.status: str | None
        self.sku: str
        self.subOrderNumber: str | None
        self.quantity: int
        self.comment: str | None
