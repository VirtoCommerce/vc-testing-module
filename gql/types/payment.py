from gql.types.base import GqlModel
from gql.types.cart_address import CartAddress
from gql.types.currency import Currency
from gql.types.money import Money


class Payment(GqlModel):
    id: str
    outer_id: str | None = None
    payment_gateway_code: str | None = None
    currency: Currency | None = None
    total: Money | None = None
    billing_address: CartAddress | None = None
