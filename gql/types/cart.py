from .base import GqlModel
from .cart_address import CartAddress
from .coupon import Coupon
from .gift_item import GiftItem
from .line_item import LineItem
from .money import Money
from .payment import Payment
from .shipment import Shipment
from .validation_error import ValidationError


class Cart(GqlModel):
    id: str
    store_id: str
    is_anonymous: bool
    has_physical_products: bool
    customer_id: str
    total: Money
    sub_total: Money
    sub_total_discount: Money
    shipping_total: Money
    items_count: int
    items_quantity: int
    items: list[LineItem]
    payments: list[Payment] = []
    shipments: list[Shipment] = []
    coupons: list[Coupon] = []
    gifts: list[GiftItem] = []
    addresses: list[CartAddress] = []
    validation_errors: list[ValidationError] = []
