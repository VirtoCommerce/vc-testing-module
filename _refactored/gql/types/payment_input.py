from gql.types.base import GqlModel
from gql.types.cart_address import CartAddress


class PaymentInput(GqlModel):
    id: str | None = None
    payment_gateway_code: str | None = None
    billing_address: CartAddress | None = None
