"""REST API operations for VirtoCommerce CMS content (pages/blogs/themes folders+files)
and menu link lists.

Endpoints verified from Katalon Object Repository
(Object Repository/API/backWebServices/VirtoCommerce.Content/*.rs):

CMS file/folder content (`/api/content/{contentType}/{storeId}`):
  POST   /folder                                  — create folder           (ContentFolderCreate)
  POST   ?folderUrl={folder}                      — upload file (multipart) (ContentFileNew)
  GET    ?relativeUrl={path}                      — get file/folder data    (ContentGet)
  GET    /search?keyword={kw}                     — search by keyword       (ContentSearch)
  GET    /move?oldUrl=&newUrl=                    — rename/move (yes, GET)  (ContentMove)
  GET    /unpack?archivePath=&destPath=           — unpack zip archive      (ContentUnpack)
  DELETE ?urls={path}                             — delete file or folder   (ContentDelete)

Store stats:
  GET    /api/content/{storeId}/stats             — pages/blogs/themes counts (ContentStatsStoreGet)

Menu link lists (`/api/cms/{storeId}/menu`):
  GET    /api/cms/{storeId}/menu                  — list all                (MenuLinkGet)
  GET    /api/cms/{storeId}/menu/{listId}         — get by id               (MenuLinkIdGet)
  POST   /api/cms/{storeId}/menu                  — create or update        (MenuLinkCreateUpdate)
  DELETE /api/cms/{storeId}/menu?listIds=         — delete                  (MenuLinkDelete)
  GET    /api/cms/{storeId}/menu/checkname?name=&language= — name available (MenuLinkCheckname)
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class CmsContentOperations(RestBaseOperations):
    """File/folder operations on a store's `pages`, `blogs`, or `themes` content type."""

    def _base(self, content_type: str, store_id: str) -> str:
        return self._url(f"/api/content/{content_type}/{store_id}")

    def get_stats(self, store_id: str) -> dict:
        return self._client.get(self._url(f"/api/content/{store_id}/stats"))

    def create_folder(self, *, content_type: str, store_id: str, folder_name: str) -> dict | None:
        return self._client.post(
            f"{self._base(content_type, store_id)}/folder",
            json={"name": folder_name, "type": "folder"},
        )

    def upload_file(
        self,
        *,
        content_type: str,
        store_id: str,
        folder_url: str,
        file_name: str,
        file_bytes: bytes,
        file_content_type: str = "application/octet-stream",
    ) -> Any:
        return self._client.post_multipart(
            self._base(content_type, store_id),
            params={"folderUrl": folder_url},
            files={"file": (file_name, file_bytes, file_content_type)},
        )

    def get(self, *, content_type: str, store_id: str, relative_url: str) -> Any:
        return self._client.get(
            self._base(content_type, store_id),
            params={"relativeUrl": relative_url},
        )

    def search(self, *, content_type: str, store_id: str, keyword: str) -> list[dict]:
        return self._client.get(
            f"{self._base(content_type, store_id)}/search",
            params={"keyword": keyword},
        )

    def move(self, *, content_type: str, store_id: str, old_url: str, new_url: str) -> Any:
        return self._client.get(
            f"{self._base(content_type, store_id)}/move",
            params={"oldUrl": old_url, "newUrl": new_url},
        )

    def unpack(self, *, content_type: str, store_id: str, archive_path: str, dest_path: str) -> Any:
        return self._client.get(
            f"{self._base(content_type, store_id)}/unpack",
            params={"archivePath": archive_path, "destPath": dest_path},
        )

    def delete(self, *, content_type: str, store_id: str, urls: str | list[str]) -> None:
        urls_param = urls if isinstance(urls, list) else [urls]
        self._client.delete(self._base(content_type, store_id), params={"urls": urls_param})


class MenuLinkOperations(RestBaseOperations):
    """Operations on store menu link lists."""

    def _base(self, store_id: str) -> str:
        return self._url(f"/api/cms/{store_id}/menu")

    def get_all(self, store_id: str) -> list[dict] | None:
        return self._client.get(self._base(store_id))

    def get_by_id(self, *, store_id: str, list_id: str) -> dict | None:
        return self._client.get(f"{self._base(store_id)}/{list_id}")

    def create_or_update(
        self,
        *,
        store_id: str,
        list_id: str,
        name: str,
        language: str = "en-US",
        menu_links: list[dict] | None = None,
    ) -> Any:
        return self._client.post(
            self._base(store_id),
            json={
                "id": list_id,
                "name": name,
                "storeId": store_id,
                "language": language,
                "menuLinks": menu_links or [],
            },
        )

    def delete(self, *, store_id: str, list_ids: str | list[str]) -> None:
        # NB: the .rs file documents `?listIds=` but the current platform expects `?ids=`;
        # `listIds` triggers a 500 NullReferenceException in the controller.
        ids_param = list_ids if isinstance(list_ids, list) else [list_ids]
        self._client.delete(self._base(store_id), params={"ids": ids_param})

    def checkname(self, *, store_id: str, name: str, language: str = "en-US") -> dict:
        return self._client.get(
            f"{self._base(store_id)}/checkname",
            params={"name": name, "language": language},
        )
