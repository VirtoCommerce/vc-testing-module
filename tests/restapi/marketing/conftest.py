"""Marketing module fixtures."""

import logging
import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.operations import (
    ContentFolderOperations,
    ContentItemOperations,
    ContentPlaceOperations,
    ContentPublicationOperations,
    CouponOperations,
    PromotionOperations,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def content_item_ops(rest_client: RestClient, backend_base_url: str) -> ContentItemOperations:
    return ContentItemOperations(rest_client, backend_base_url)


@pytest.fixture
def content_folder_ops(rest_client: RestClient, backend_base_url: str) -> ContentFolderOperations:
    return ContentFolderOperations(rest_client, backend_base_url)


@pytest.fixture
def content_place_ops(rest_client: RestClient, backend_base_url: str) -> ContentPlaceOperations:
    return ContentPlaceOperations(rest_client, backend_base_url)


@pytest.fixture
def content_pub_ops(rest_client: RestClient, backend_base_url: str) -> ContentPublicationOperations:
    return ContentPublicationOperations(rest_client, backend_base_url)


@pytest.fixture
def promo_ops(rest_client: RestClient, backend_base_url: str) -> PromotionOperations:
    return PromotionOperations(rest_client, backend_base_url)


@pytest.fixture
def coupon_ops(rest_client: RestClient, backend_base_url: str) -> CouponOperations:
    return CouponOperations(rest_client, backend_base_url)


@pytest.fixture
def make_content_item(content_item_ops: ContentItemOperations) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAItem_{uuid.uuid4().hex[:8]}")
        item = content_item_ops.create(name=name, **overrides)
        created_ids.append(item["id"])
        return item

    yield _make
    for iid in reversed(created_ids):
        try:
            content_item_ops.delete(iid)
        except Exception as e:
            logger.warning("Cleanup failed for content item %s: %s", iid, e)


@pytest.fixture
def make_content_folder(content_folder_ops: ContentFolderOperations) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAFolder_{uuid.uuid4().hex[:8]}")
        folder = content_folder_ops.create(name=name, **overrides)
        created_ids.append(folder["id"])
        return folder

    yield _make
    for fid in reversed(created_ids):
        try:
            content_folder_ops.delete(fid)
        except Exception as e:
            logger.warning("Cleanup failed for content folder %s: %s", fid, e)


@pytest.fixture
def make_content_place(content_place_ops: ContentPlaceOperations) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAPlace_{uuid.uuid4().hex[:8]}")
        place = content_place_ops.create(name=name, **overrides)
        created_ids.append(place["id"])
        return place

    yield _make
    for pid in reversed(created_ids):
        try:
            content_place_ops.delete(pid)
        except Exception as e:
            logger.warning("Cleanup failed for content place %s: %s", pid, e)


@pytest.fixture
def make_content_publication(
    content_pub_ops: ContentPublicationOperations,
) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAPub_{uuid.uuid4().hex[:8]}")
        pub = content_pub_ops.create(name=name, **overrides)
        created_ids.append(pub["id"])
        return pub

    yield _make
    for pid in reversed(created_ids):
        try:
            content_pub_ops.delete(pid)
        except Exception as e:
            logger.warning("Cleanup failed for content publication %s: %s", pid, e)


@pytest.fixture
def make_promotion(promo_ops: PromotionOperations) -> Generator[Callable[..., dict], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAPromo_{uuid.uuid4().hex[:8]}")
        promo = promo_ops.create(name=name, **overrides)
        created_ids.append(promo["id"])
        return promo

    yield _make
    for pid in reversed(created_ids):
        try:
            promo_ops.delete(pid)
        except Exception as e:
            logger.warning("Cleanup failed for promotion %s: %s", pid, e)
