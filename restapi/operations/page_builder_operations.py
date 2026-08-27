"""REST API operations for PageBuilderModule grouped pages.

Endpoints verified against the module's swagger
(``/docs/VirtoCommerce.PageBuilderModule/swagger.json``):
  POST   /api/page-builder-pages/search                                — search
  GET    /api/page-builder-pages/grouped/{groupId}                     — get by id
  DELETE /api/page-builder-pages/grouped/{groupId}                     — hard delete
  POST   /api/page-builder-pages/grouped/archive?ids=                  — archive
  POST   /api/page-builder-pages/grouped/publishing/{groupId}?publish= — publish

The grouped page **id** returned by search is the ``groupId`` the other
endpoints take; there is no separate lookup.
"""

from restapi.operations.base import RestBaseOperations
from restapi.types.page_builder import PageBuilderPage


class PageBuilderOperations(RestBaseOperations):
    PATH = "/api/page-builder-pages"
    GROUPED = f"{PATH}/grouped"

    def search(
        self,
        *,
        store_id: str,
        keyword: str | None = None,
        skip: int = 0,
        take: int = 1000,
    ) -> list[PageBuilderPage]:
        """Search grouped pages.

        No ``sort`` is sent on purpose: the backend applies the keyword filter
        to the sorted window rather than the whole set, so a sorted keyword
        search silently misses rows outside that window.
        """
        payload: dict[str, object] = {"storeId": store_id, "skip": skip, "take": take}
        if keyword:
            payload["keyword"] = keyword
        response = self._client.post(self._url(f"{self.PATH}/search"), json=payload)
        results = response.get("results", []) if isinstance(response, dict) else (response or [])
        return [PageBuilderPage.model_validate(item) for item in results]

    def get(self, group_id: str) -> PageBuilderPage:
        response = self._client.get(self._url(f"{self.GROUPED}/{group_id}"))
        return PageBuilderPage.model_validate(response)

    def delete(self, group_id: str) -> None:
        self._client.delete(self._url(f"{self.GROUPED}/{group_id}"))

    def archive(self, *group_ids: str) -> None:
        self._client.post(self._url(f"{self.GROUPED}/archive"), json={}, params={"ids": list(group_ids)})

    def publish(self, group_id: str, publish: bool = True) -> None:
        self._client.post(
            self._url(f"{self.GROUPED}/publishing/{group_id}"),
            json={},
            params={"publish": str(publish).lower()},
        )
