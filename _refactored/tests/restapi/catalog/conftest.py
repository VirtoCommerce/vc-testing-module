"""Catalog module fixtures — factory fixtures for catalogs, categories, products."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.operations import CatalogOperations, CategoryOperations, ProductOperations


@pytest.fixture
def catalog_ops(rest_client: RestClient, backend_base_url: str) -> CatalogOperations:
    return CatalogOperations(rest_client, backend_base_url)


@pytest.fixture
def category_ops(rest_client: RestClient, backend_base_url: str) -> CategoryOperations:
    return CategoryOperations(rest_client, backend_base_url)


@pytest.fixture
def product_ops(rest_client: RestClient, backend_base_url: str) -> ProductOperations:
    return ProductOperations(rest_client, backend_base_url)


@pytest.fixture
def make_catalog(catalog_ops: CatalogOperations) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh catalog per call, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QACatalog_{uuid.uuid4().hex[:8]}")
        catalog = catalog_ops.create(name=name, **overrides)
        created_ids.append(catalog["id"])
        return catalog

    yield _make

    for cid in reversed(created_ids):
        try:
            catalog_ops.delete(cid)
        except Exception:
            pass


@pytest.fixture
def make_category(
    category_ops: CategoryOperations,
    make_catalog: Callable[..., dict],
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a category (and implicit catalog if needed), cleans up at teardown."""
    created_ids: list[str] = []

    def _make(*, catalog: dict | None = None, **overrides: Any) -> dict:
        if catalog is None:
            catalog = make_catalog()
        name = overrides.pop("name", f"QACategory_{uuid.uuid4().hex[:8]}")
        code = overrides.pop("code", f"qa-cat-{uuid.uuid4().hex[:6]}")
        category = category_ops.create(catalog_id=catalog["id"], name=name, code=code, **overrides)
        created_ids.append(category["id"])
        return category

    yield _make

    for cid in reversed(created_ids):
        try:
            category_ops.delete(cid)
        except Exception:
            pass


@pytest.fixture
def make_product(
    product_ops: ProductOperations,
    make_category: Callable[..., dict],
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a product (and implicit catalog+category if needed), cleans up at teardown."""
    created_ids: list[str] = []

    def _make(*, category: dict | None = None, **overrides: Any) -> dict:
        if category is None:
            category = make_category()
        name = overrides.pop("name", f"QAProduct_{uuid.uuid4().hex[:8]}")
        code = overrides.pop("code", f"QA-SKU-{uuid.uuid4().hex[:8].upper()}")
        product = product_ops.create(
            catalog_id=category["catalogId"],
            category_id=category["id"],
            name=name,
            code=code,
            **overrides,
        )
        created_ids.append(product["id"])
        return product

    yield _make

    for pid in reversed(created_ids):
        try:
            product_ops.delete(pid)
        except Exception:
            pass
