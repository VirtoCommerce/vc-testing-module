"""REST API operations for VirtoCommerce promotions and coupons.

Endpoints verified from Katalon Object Repository.
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class PromotionOperations(RestBaseOperations):
    PATH = "/api/marketing/promotions"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"name": name, "isActive": True, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, promo: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**promo, **overrides})

    def get_by_id(self, promo_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{promo_id}"))

    def get_new(self) -> dict:
        return self._client.get(self._url(f"{self.PATH}/new"))

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(self._url(f"{self.PATH}/search"), json={"skip": skip, "take": take, **extra})

    def delete(self, *promo_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(promo_ids)})


class CouponOperations(RestBaseOperations):
    PATH = "/api/marketing/promotions/coupons"

    def add(self, coupons: list[dict]) -> None:
        """POST /api/marketing/promotions/coupons/add."""
        self._client.post(self._url(f"{self.PATH}/add"), json=coupons)

    def get_by_id(self, coupon_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{coupon_id}"))

    def search(self, *, promotion_id: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if promotion_id:
            payload["promotionId"] = promotion_id
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *coupon_ids: str) -> None:
        self._client.delete(self._url(f"{self.PATH}/delete"), params={"ids": list(coupon_ids)})
