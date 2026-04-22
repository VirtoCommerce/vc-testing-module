"""Product CRUD — migrated from Katalon `API Coverage/ModuleCatalog/product*`.

Originals:
- productCreate       → test_product_create
- productUpdate       → test_product_update
- productsGetById     → test_product_get_by_id
- productsDelete      → test_product_delete

Key differences from Katalon:
- Each test creates its own implicit catalog+category+product via make_product.
  No cross-test state from `GlobalVariable.productId`.
- GET returns a list (the endpoint is `/api/catalog/products?ids=...`); we use
  `get_by_id` as a single-item convenience wrapper.
- Product DELETE goes through /api/catalog/listentries/delete, same as
  category DELETE.
"""

import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from webapi_operations.catalog.product_operations import ProductOperations


@pytest.mark.webapi
@allure.feature("Catalog / Products (WebAPI)")
@allure.title("Create product")
def test_product_create(make_product):
    with allure.step("POST /api/catalog/products"):
        product = make_product()

    assert product["id"], "Product id missing from create response"
    assert product["name"].startswith("QAProduct_"), f"Unexpected name: {product['name']}"
    assert product["code"].startswith("QA-SKU-"), f"Unexpected code: {product['code']}"
    assert product["catalogId"], "catalogId missing"
    assert product["categoryId"], "categoryId missing"


@pytest.mark.webapi
@allure.feature("Catalog / Products (WebAPI)")
@allure.title("Update product — rename and change dimensions")
def test_product_update(make_product, product_operations: ProductOperations):
    product = make_product()
    new_name = f"{product['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"POST /api/catalog/products — rename to {new_name}, weight=2.5"):
        product_operations.update(product, name=new_name, weight="2.5")

    with allure.step("Verify update via GET"):
        reloaded = product_operations.get_by_id(product["id"])
        assert reloaded["name"] == new_name
        assert reloaded["weight"] == 2.5 or reloaded["weight"] == "2.5"


@pytest.mark.webapi
@allure.feature("Catalog / Products (WebAPI)")
@allure.title("Get product by id")
def test_product_get_by_id(make_product, product_operations: ProductOperations):
    product = make_product()

    with allure.step(f"GET /api/catalog/products?ids={product['id']}"):
        reloaded = product_operations.get_by_id(product["id"])

    assert reloaded["id"] == product["id"]
    assert reloaded["name"] == product["name"]
    assert reloaded["code"] == product["code"]


@pytest.mark.webapi
@allure.feature("Catalog / Products (WebAPI)")
@allure.title("Delete product")
def test_product_delete(make_product, product_operations: ProductOperations):
    product = make_product()

    with allure.step(f"POST /api/catalog/listentries/delete — objectIds=[{product['id']}]"):
        product_operations.delete(product["id"])

    with allure.step("Verify product no longer returned by GET"):
        try:
            results = product_operations.get_by_ids([product["id"]])
        except HTTPError as e:
            assert e.response.status_code in (404, 204)
        else:
            # Backend often returns empty array rather than 404.
            ids = [r.get("id") for r in (results or [])]
            assert product["id"] not in ids, f"Product still returned after delete: {results}"
