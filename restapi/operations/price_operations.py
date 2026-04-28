"""REST API operations for VirtoCommerce prices.

Endpoints verified from Katalon Object Repository:
  PUT    /api/products/prices                                   — add prices to pricelist
  PUT    /api/products/{productId}/prices                       — add/update by product
  DELETE /api/pricing/products/prices?priceIds=                 — delete by price id
  DELETE /api/pricing/pricelists/{id}/products/prices?productIds= — delete by pricelist+product
  GET    /api/products/{productId}/{catalogId}/pricesWidget     — prices widget
  GET    /api/catalog/products/prices/search?pricelistId=       — search GET
  POST   /api/catalog/products/prices/search                    — search POST
  GET    /api/catalog/products/{productId}/pricelists           — get pricelists for product
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class PriceOperations(RestBaseOperations):

    def add_prices(self, prices: list[dict]) -> None:
        """PUT /api/products/prices — Katalon wraps in [{"prices": [...]}]."""
        self._client.put(self._url("/api/products/prices"), json=[{"prices": prices}])

    def add_update_by_product(self, product_id: str, prices: list[dict]) -> None:
        """PUT /api/products/{productId}/prices."""
        self._client.put(self._url(f"/api/products/{product_id}/prices"), json=[{"prices": prices}])

    def delete_by_price_id(self, *price_ids: str) -> None:
        """DELETE /api/pricing/products/prices?priceIds=..."""
        self._client.delete(self._url("/api/pricing/products/prices"), params={"priceIds": list(price_ids)})

    def delete_by_pricelist_and_product(self, pricelist_id: str, *product_ids: str) -> None:
        """DELETE /api/pricing/pricelists/{id}/products/prices?productIds=..."""
        self._client.delete(
            self._url(f"/api/pricing/pricelists/{pricelist_id}/products/prices"),
            params={"productIds": list(product_ids)},
        )

    def get_widget(self, product_id: str, catalog_id: str) -> dict:
        """GET /api/products/{productId}/{catalogId}/pricesWidget."""
        return self._client.get(self._url(f"/api/products/{product_id}/{catalog_id}/pricesWidget"))

    def search_get(self, *, pricelist_id: str) -> dict | list:
        """GET /api/catalog/products/prices/search?pricelistId=..."""
        return self._client.get(self._url("/api/catalog/products/prices/search"), params={"pricelistId": pricelist_id})

    def search_post(
        self, *, pricelist_ids: list[str] | None = None, skip: int = 0, take: int = 20, **extra: Any
    ) -> dict:
        """POST /api/catalog/products/prices/search."""
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if pricelist_ids:
            payload["pricelistIds"] = pricelist_ids
        return self._client.post(self._url("/api/catalog/products/prices/search"), json=payload)

    def get_product_pricelists(self, product_id: str) -> list[dict]:
        """GET /api/catalog/products/{productId}/pricelists."""
        return self._client.get(self._url(f"/api/catalog/products/{product_id}/pricelists"))
