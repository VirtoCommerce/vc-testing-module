from pydantic import BaseModel


class OrderShipmentPackageType(BaseModel):
    def __init__(self):
        from graphql_client.types.order_shipment_item_type import OrderShipmentItemType
        from decimal import Decimal

        self.id: str
        self.barCode: str | None
        self.packageType: str | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.measureUnit: str | None
        self.height: Decimal | None
        self.length: Decimal | None
        self.width: Decimal | None
        self.items: list[OrderShipmentItemType]
