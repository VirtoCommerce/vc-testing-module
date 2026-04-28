"""Content module fixtures — operations + factory fixtures + blacklist setup."""

import uuid
from collections.abc import Callable, Generator
from typing import Any

import pytest

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from restapi.operations import CmsContentOperations, MenuLinkOperations, SettingsOperations


_FILE_EXTENSIONS_BLACKLIST_SETTING = "VirtoCommerce.Platform.Security.FileExtensionsBlackList"
_FORBIDDEN_EXTENSION = ".exe"


@pytest.fixture
def cms_content_ops(rest_client: RestClient, backend_base_url: str) -> CmsContentOperations:
    return CmsContentOperations(rest_client, backend_base_url)


@pytest.fixture
def menu_ops(rest_client: RestClient, backend_base_url: str) -> MenuLinkOperations:
    return MenuLinkOperations(rest_client, backend_base_url)


@pytest.fixture
def store_id(global_settings: GlobalSettings) -> str:
    return global_settings.store_id


@pytest.fixture
def make_content_folder(
    cms_content_ops: CmsContentOperations, store_id: str
) -> Generator[Callable[..., dict], None, None]:
    """Factory: create a folder under a content type, deletes it (and contents) at teardown."""
    created: list[tuple[str, str]] = []  # (content_type, folder_name)

    def _make(*, content_type: str, name: str | None = None) -> dict[str, Any]:
        folder_name = name or f"qa-folder-{uuid.uuid4().hex[:8]}"
        cms_content_ops.create_folder(content_type=content_type, store_id=store_id, folder_name=folder_name)
        created.append((content_type, folder_name))
        return {"contentType": content_type, "folderName": folder_name}

    yield _make

    for content_type, folder_name in reversed(created):
        try:
            cms_content_ops.delete(content_type=content_type, store_id=store_id, urls=folder_name)
        except Exception:
            pass


@pytest.fixture
def make_menu_link_list(menu_ops: MenuLinkOperations, store_id: str) -> Generator[Callable[..., dict], None, None]:
    """Factory: create a menu link list, deletes it at teardown."""
    created_ids: list[str] = []

    def _make(*, name: str | None = None, language: str = "en-US", menu_links: list[dict] | None = None) -> dict:
        list_id = str(uuid.uuid4())
        menu_name = name or f"QAMenu_{uuid.uuid4().hex[:6]}"
        menu_ops.create_or_update(
            store_id=store_id,
            list_id=list_id,
            name=menu_name,
            language=language,
            menu_links=menu_links,
        )
        created_ids.append(list_id)
        return {"id": list_id, "name": menu_name, "language": language}

    yield _make

    for lid in reversed(created_ids):
        try:
            menu_ops.delete(store_id=store_id, list_ids=lid)
        except Exception:
            pass


@pytest.fixture(scope="session")
def ensure_exe_in_blacklist(
    global_settings: GlobalSettings, admin_auth, backend_base_url: str
) -> Generator[None, None, None]:
    """Ensure `.exe` is in the platform's file-extensions blacklist for upload tests.

    Mutates a global setting — tests that depend on this fixture must be marked
    `@pytest.mark.serial`. Reverts to the original list at session end.
    """
    with RestClient(global_settings=global_settings, auth=admin_auth) as client:
        ops = SettingsOperations(client, backend_base_url)
        original = ops.get_by_name(_FILE_EXTENSIONS_BLACKLIST_SETTING)
        original_values = list(original.get("allowedValues") or [])
        if _FORBIDDEN_EXTENSION not in original_values:
            updated = {**original, "allowedValues": [*original_values, _FORBIDDEN_EXTENSION]}
            ops.update([updated])

        yield

        if _FORBIDDEN_EXTENSION not in original_values:
            reverted = {**original, "allowedValues": original_values}
            ops.update([reverted])
