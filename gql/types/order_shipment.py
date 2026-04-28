from .base import GqlModel
from .money import Money


class OrderShipment(GqlModel):
    id: str
    number: str
    shipment_method_code: str | None = None
    shipment_method_option: str | None = None
    status: str | None = None
    total: Money
