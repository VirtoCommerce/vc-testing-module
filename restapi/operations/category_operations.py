"""REST API operations for VirtoCommerce catalog categories."""

from typing import Any

from restapi.constants import CATEGORY_TEMPLATE
from restapi.operations.base import RestBaseOperations
from restapi.types import Category


class CategoryOperations(RestBaseOperations):
    PATH = "/api/catalog/categories"
    LIST_ENTRIES = "/api/catalog/listentries"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"

    def create(self, *, catalog_id: str, name: str, code: str, **overrides: Any) -> Category:
        payload = {**CATEGORY_TEMPLATE, "catalogId": catalog_id, "name": name, "code": code, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Category.model_validate(response)

    def get_by_id(self, category_id: str) -> Category:
        response = self._client.get(self._url(f"{self.PATH}/{category_id}"))
        return Category.model_validate(response)

    def get_new_template(self, catalog_id: str) -> dict:
        return self._client.get(self._url(f"/api/catalog/{catalog_id}/categories/newcategory"))

    def update(self, category: Category, **overrides: Any) -> Category:
        existing = category.model_dump(by_alias=True, exclude_none=True)
        payload = {**CATEGORY_TEMPLATE, **existing, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Category.model_validate(response)

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
