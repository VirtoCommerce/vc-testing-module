import uuid
from typing import Any, Callable

import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from webapi_operations.catalog.catalog_operations import CatalogOperations
from webapi_operations.catalog.category_operations import CategoryOperations
from webapi_operations.catalog.product_operations import ProductOperations


# ---------------------------------------------------------------- ops fixtures


@pytest.fixture
def catalog_operations(webapi_client: WebAPISession) -> CatalogOperations:
    return CatalogOperations(webapi_client)


@pytest.fixture
def category_operations(webapi_client: WebAPISession) -> CategoryOperations:
    return CategoryOperations(webapi_client)


@pytest.fixture
def product_operations(webapi_client: WebAPISession) -> ProductOperations:
    return ProductOperations(webapi_client)


# ---------------------------------------------------------------- factories


@pytest.fixture
def make_catalog(
    catalog_operations: CatalogOperations,
    auth: Auth,
    config: Config,
) -> Callable[..., dict]:
    """Factory that creates a fresh catalog per call and cleans up at teardown.

    Usage:
        def test_x(make_catalog):
            catalog = make_catalog()                    # default name + template
            catalog = make_catalog(name="custom")       # override name
            catalog = make_catalog(isVirtual=True)      # override template field

    Authenticates once per worker (idempotent check avoids hammering /connect/token).
    Cleanup silently swallows errors so a test failure can't leak into teardown.
    """
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        if auth.token_data is None or not auth.token_data.access_token:
            auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        name = overrides.pop("name", f"QACatalog_{uuid.uuid4().hex[:8]}")
        catalog = catalog_operations.create(name=name, **overrides)
        created_ids.append(catalog["id"])
        return catalog

    yield _make

    for cid in created_ids:
        try:
            catalog_operations.delete(cid)
        except Exception:
            pass


@pytest.fixture
def make_category(
    category_operations: CategoryOperations,
    make_catalog: Callable[..., dict],
) -> Callable[..., dict]:
    """Factory for categories.

    Usage:
        category = make_category()                       # creates implicit fresh catalog
        category = make_category(catalog=some_catalog)   # reuse an existing catalog

    Teardown deletes all created categories BEFORE make_catalog deletes the
    catalog (pytest fixture teardown is LIFO, so this ordering is automatic).
    """
    created_ids: list[str] = []

    def _make(*, catalog: dict | None = None, **overrides: Any) -> dict:
        if catalog is None:
            catalog = make_catalog()
        name = overrides.pop("name", f"QACategory_{uuid.uuid4().hex[:8]}")
        code = overrides.pop("code", f"qa-cat-{uuid.uuid4().hex[:6]}")
        category = category_operations.create(catalog_id=catalog["id"], name=name, code=code, **overrides)
        created_ids.append(category["id"])
        return category

    yield _make

    for cid in created_ids:
        try:
            category_operations.delete(cid)
        except Exception:
            pass


@pytest.fixture
def make_product(
    product_operations: ProductOperations,
    make_category: Callable[..., dict],
) -> Callable[..., dict]:
    """Factory for products.

    Usage:
        product = make_product()                          # fresh catalog + fresh category
        product = make_product(category=some_category)    # reuse an existing category

    Teardown order: products delete first, then categories, then catalog.
    """
    created_ids: list[str] = []

    def _make(*, category: dict | None = None, **overrides: Any) -> dict:
        if category is None:
            category = make_category()
        name = overrides.pop("name", f"QAProduct_{uuid.uuid4().hex[:8]}")
        code = overrides.pop("code", f"QA-SKU-{uuid.uuid4().hex[:8].upper()}")
        product = product_operations.create(
            catalog_id=category["catalogId"],
            category_id=category["id"],
            name=name,
            code=code,
            **overrides,
        )
        created_ids.append(product["id"])
        return product

    yield _make

    for pid in created_ids:
        try:
            product_operations.delete(pid)
        except Exception:
            pass
