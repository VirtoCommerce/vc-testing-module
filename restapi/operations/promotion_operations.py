"""REST API operations for VirtoCommerce promotions and coupons.

Endpoints verified from Katalon Object Repository.
"""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import Promotion


class PromotionOperations(RestBaseOperations):
    PATH = "/api/marketing/promotions"

    def create(self, *, name: str, **overrides: Any) -> Promotion:
        payload: dict[str, Any] = {"name": name, "isActive": True, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Promotion.model_validate(response)

    def update(self, promo: Promotion, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = promo.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def get_by_id(self, promo_id: str) -> Promotion:
        response = self._client.get(self._url(f"{self.PATH}/{promo_id}"))
        return Promotion.model_validate(response)

    def get_new(self) -> dict:
        """GET /api/marketing/promotions/new — partial template, dict."""
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
