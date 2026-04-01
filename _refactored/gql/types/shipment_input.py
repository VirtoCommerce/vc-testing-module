from gql.types.base import GqlModel
from gql.types.cart_address import CartAddress


class ShipmentInput(GqlModel):
    id: str | None = None
    shipment_method_code: str | None = None
    shipment_method_option: str | None = None
    fulfillment_center_id: str | None = None
    price: float | None = None
    currency: str | None = None
    comment: str | None = None
    delivery_address: CartAddress | None = None
    height: float | None = None
    length: float | None = None
    width: float | None = None
    weight: float | None = None
    measure_unit: str | None = None
    weight_unit: str | None = None
