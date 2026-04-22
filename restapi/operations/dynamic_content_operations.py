"""REST API operations for VirtoCommerce Marketing dynamic content.

Covers content items, folders, placeholders (places), and publications.
All endpoints verified from Katalon Object Repository.
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class ContentItemOperations(RestBaseOperations):
    PATH = "/api/marketing/contentitems"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, item: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**item, **overrides})

    def get_by_id(self, item_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{item_id}"))

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(self._url(f"{self.PATH}/search"), json={"skip": skip, "take": take, **extra})

    def list_entries_search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(
            self._url(f"{self.PATH}/listentries/search"), json={"skip": skip, "take": take, **extra}
        )

    def evaluate(self, criteria: dict) -> list[dict]:
        return self._client.post(self._url(f"{self.PATH}/evaluate"), json=criteria)

    def delete(self, *item_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(item_ids)})


class ContentFolderOperations(RestBaseOperations):
    PATH = "/api/marketing/contentfolders"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, folder: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**folder, **overrides})

    def get_by_id(self, folder_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{folder_id}"))

    def delete(self, *folder_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(folder_ids)})


class ContentPlaceOperations(RestBaseOperations):
    PATH = "/api/marketing/contentplaces"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, place: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**place, **overrides})

    def get_by_id(self, place_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{place_id}"))

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(self._url(f"{self.PATH}/search"), json={"skip": skip, "take": take, **extra})

    def list_entries_search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(
            self._url(f"{self.PATH}/listentries/search"), json={"skip": skip, "take": take, **extra}
        )

    def delete(self, *place_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(place_ids)})


class ContentPublicationOperations(RestBaseOperations):
    PATH = "/api/marketing/contentpublications"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, publication: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**publication, **overrides})

    def get_by_id(self, pub_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{pub_id}"))

    def get_new(self) -> dict:
        return self._client.get(self._url(f"{self.PATH}/new"))

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        return self._client.post(self._url(f"{self.PATH}/search"), json={"skip": skip, "take": take, **extra})

    def delete(self, *pub_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(pub_ids)})
