from .base import GqlModel


class Coupon(GqlModel):
    code: str
    is_applied_successfully: bool
