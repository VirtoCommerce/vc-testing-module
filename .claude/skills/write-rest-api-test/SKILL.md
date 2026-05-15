---
name: write-rest-api-test
description: "Scaffold REST API test files and factory fixture conftest files — admin auth, RestClient, factory fixtures with auto-teardown, Allure steps, CRUD patterns"
argument-hint: "<module> <entity>"
---

## REST API Test Scaffolding

When writing a REST API test, follow these patterns exactly.

## Required Imports

```python
import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from restapi.operations import ProductOperations  # domain-specific operations
```

## Allure Conventions

```python
@allure.feature("<Module> / <Entity> (REST API)")  # e.g., "Catalog / Products (REST API)"
@allure.title("<Action>")                           # e.g., "Create product"
with allure.step("<HTTP method> <endpoint>"):        # e.g., "POST /api/catalog/products"
with allure.step("Verify response"):                 # verification step
```

## Complete CRUD Test Example

```python
@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Create product")
def test_product_create(make_product):
    with allure.step("POST /api/catalog/products"):
        product = make_product()

    with allure.step("Verify response"):
        assert product["id"], "Product id missing"
        assert product["name"].startswith("QAProduct_")
        assert product["code"].startswith("QA-SKU-")
        assert product["catalogId"]
        assert product["categoryId"]


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Update product — rename and change dimensions")
def test_product_update(make_product, product_ops: ProductOperations):
    product = make_product()
    new_name = f"{product['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"POST /api/catalog/products — rename to {new_name}, weight=2.5"):
        product_ops.update(product, name=new_name, weight="2.5")

    with allure.step("Verify update via GET"):
        reloaded = product_ops.get_by_id(product["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Get product by id")
def test_product_get_by_id(make_product, product_ops: ProductOperations):
    product = make_product()

    with allure.step(f"GET /api/catalog/products?ids={product['id']}"):
        reloaded = product_ops.get_by_id(product["id"])

    with allure.step("Verify fields match"):
        assert reloaded["id"] == product["id"]
        assert reloaded["name"] == product["name"]
        assert reloaded["code"] == product["code"]


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Delete product")
def test_product_delete(make_product, product_ops: ProductOperations):
    product = make_product()

    with allure.step(f"POST /api/catalog/listentries/delete — objectIds=[{product['id']}]"):
        product_ops.delete(product["id"])

    with allure.step("Verify product no longer returned by GET"):
        try:
            results = product_ops.get_by_ids([product["id"]])
        except HTTPError as e:
            assert e.response.status_code in (404, 204)
        else:
            ids = [r.get("id") for r in (results or [])]
            assert product["id"] not in ids
```

## Conftest Layering

REST API tests use two levels of conftest:

### Level 1: `tests/restapi/conftest.py` — shared admin auth and client

```python
from typing import Generator
import pytest
from core.auth import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings

@pytest.fixture(scope="session")
def admin_auth(global_settings: GlobalSettings) -> AuthProvider:
    provider = AuthProvider(global_settings.backend_base_url)
    provider.sign_in(global_settings.admin_username, global_settings.admin_password)
    return provider

@pytest.fixture
def rest_client(global_settings: GlobalSettings, admin_auth: AuthProvider) -> Generator[RestClient, None, None]:
    with RestClient(global_settings=global_settings, auth=admin_auth) as client:
        yield client

@pytest.fixture(scope="session")
def backend_base_url(global_settings: GlobalSettings) -> str:
    return global_settings.backend_base_url
```

### Level 2: `tests/restapi/<module>/conftest.py` — factory fixtures

```python
import uuid
from typing import Any, Callable, Generator
import pytest
from core.clients.rest import RestClient
from restapi.operations import CatalogOperations, CategoryOperations, ProductOperations

@pytest.fixture
def catalog_ops(rest_client: RestClient, backend_base_url: str) -> CatalogOperations:
    return CatalogOperations(rest_client, backend_base_url)

@pytest.fixture
def product_ops(rest_client: RestClient, backend_base_url: str) -> ProductOperations:
    return ProductOperations(rest_client, backend_base_url)

@pytest.fixture
def make_product(
    product_ops: ProductOperations,
    make_category: Callable[..., dict],
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a product per call, auto-cleans at teardown."""
    created_ids: list[str] = []

    def _make(*, category: dict | None = None, **overrides: Any) -> dict:
        if category is None:
            category = make_category()
        name = overrides.pop("name", f"QAProduct_{uuid.uuid4().hex[:8]}")
        code = overrides.pop("code", f"QA-SKU-{uuid.uuid4().hex[:8].upper()}")
        product = product_ops.create(
            catalog_id=category["catalogId"],
            category_id=category["id"],
            name=name, code=code, **overrides,
        )
        created_ids.append(product["id"])
        return product

    yield _make

    for pid in created_ids:
        try:
            product_ops.delete(pid)
        except Exception:
            pass
```

## Factory Fixture Pattern

The factory pattern is the standard for REST API test fixtures:

1. **Operations fixture** — function-scoped, wraps RestClient + backend URL
2. **Factory fixture** — yields a callable `_make(**overrides)`, tracks created IDs, deletes all at teardown
3. **Chained factories** — `make_product` depends on `make_category` which depends on `make_catalog`
4. **Silent cleanup** — `except Exception: pass` in teardown loops
5. **Default names** — `f"QA{Entity}_{uuid.uuid4().hex[:8]}"` for unique resource names

## Available Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `admin_auth: AuthProvider` | session | Signed in as admin |
| `rest_client: RestClient` | function | Auto-closed via context manager |
| `backend_base_url: str` | session | For operations constructors |
| `<entity>_ops: <Entity>Operations` | function | Operations class instance |
| `make_<entity>: Callable[..., dict]` | function | Factory with auto-cleanup |

## Assertion Patterns

```python
# Raw dict assertions
assert product["id"], "Product id missing"
assert product["name"].startswith("QAProduct_")
assert reloaded["name"] == new_name

# Error assertions
from requests.exceptions import HTTPError
try:
    results = ops.get_by_ids([deleted_id])
except HTTPError as e:
    assert e.response.status_code in (404, 204)

# Truthiness for required fields
assert product["catalogId"]
assert product["categoryId"]
```

## Rules

1. Every test function MUST have `@pytest.mark.restapi`
2. Every test function MUST have `@allure.feature()` and `@allure.title()`
3. Every test body MUST use `with allure.step()` for HTTP calls and verification
4. Use factory fixtures (`make_product`) — don't manually create and clean up
5. Factory fixtures auto-create dependencies (catalog/category) if not provided
6. Return type annotation: `def test_...(fixtures) -> None:`
7. Use `@pytest.mark.serial` for tests that mutate global platform state
8. Tests work with raw dicts — not Pydantic models
9. Use `uuid.uuid4().hex[:8]` for unique names in test data
