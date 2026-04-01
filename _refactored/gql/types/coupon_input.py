from gql.types.base import GqlModel


class CouponInput(GqlModel):
    store_id: str
    user_id: str
    coupon_code: str
    culture_name: str | None = None
    currency_code: str | None = None
