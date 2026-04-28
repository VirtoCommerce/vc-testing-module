from .base import GqlModel
from .money import Money
from .order_line_item import OrderLineItem
from .order_payment import OrderPayment
from .order_shipment import OrderShipment


class Order(GqlModel):
    id: str
    number: str
    status: str | None = None
    created_date: str
    total: Money
    items: list[OrderLineItem] = []
    in_payments: list[OrderPayment] = []
    shipments: list[OrderShipment] = []
