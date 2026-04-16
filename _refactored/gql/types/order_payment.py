from .base import GqlModel
from .money import Money


class OrderPayment(GqlModel):
    id: str
    number: str
    gateway_code: str | None = None
    status: str | None = None
    sum: Money
