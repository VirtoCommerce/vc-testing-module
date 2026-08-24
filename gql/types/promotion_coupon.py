from .base import GqlModel


class PromotionCoupon(GqlModel):
    id: str
    end_date: str | None = None
    label: str | None = None
    name: str | None = None
    description: str | None = None
    coupon_code: str
