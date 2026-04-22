from gql.types.base import GqlModel
from gql.types.cart_address import CartAddress
from gql.types.currency import Currency
from gql.types.money import Money


class Shipment(GqlModel):
    id: str
    shipment_method_code: str | None = None
    shipment_method_option: str | None = None
    fulfillment_center_id: str | None = None
    price: Money | None = None
    currency: Currency | None = None
    delivery_address: CartAddress | None = None
