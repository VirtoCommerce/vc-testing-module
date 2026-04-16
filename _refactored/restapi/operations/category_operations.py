"""REST API operations for VirtoCommerce catalog categories."""

from typing import Any

from restapi.constants import CATEGORY_TEMPLATE
from restapi.operations.base import RestBaseOperations


class CategoryOperations(RestBaseOperations):
    PATH = "/api/catalog/categories"
    LIST_ENTRIES = "/api/catalog/listentries"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"

    def create(self, *, catalog_id: str, name: str, code: str, **overrides: Any) -> dict:
        payload = {**CATEGORY_TEMPLATE, "catalogId": catalog_id, "name": name, "code": code, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def get_by_id(self, category_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{category_id}"))

    def get_new_template(self, catalog_id: str) -> dict:
        return self._client.get(self._url(f"/api/catalog/{catalog_id}/categories/newcategory"))

    def update(self, category: dict, **overrides: Any) -> dict:
        payload = {**CATEGORY_TEMPLATE, **category, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def search(
        self, *, catalog_id: str, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any
    ) -> dict:
        payload: dict[str, Any] = {
            "catalogId": catalog_id,
            "responseGroup": "withCategories",
            "skip": skip,
            "take": take,
            **extra,
        }
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(self.LIST_ENTRIES), json=payload)

    def search_listentries_by_phrase(self, *, search_phrase: str, skip: int = 0, take: int = 50) -> dict:
        payload = {
            "searchPhrase": search_phrase,
            "searchInVariations": False,
            "responseGroup": "withCategories, withProducts",
            "sort": "",
            "skip": skip,
            "take": take,
        }
        return self._client.post(self._url(self.LIST_ENTRIES), json=payload)

    def delete(self, category_id: str) -> None:
        self._client.post(self._url(self.LIST_ENTRIES_DELETE), json={"objectIds": [category_id]})
