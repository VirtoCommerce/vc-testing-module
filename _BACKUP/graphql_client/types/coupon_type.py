from pydantic import BaseModel


class CouponType(BaseModel):
    def __init__(self):

        self.code: str | None
        self.isAppliedSuccessfully: bool
