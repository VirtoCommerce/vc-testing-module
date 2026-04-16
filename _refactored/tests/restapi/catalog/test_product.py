"""Product CRUD — migrated from Katalon `API Coverage/ModuleCatalog/product*`."""

import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from restapi.operations import ProductOperations


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
        assert reloaded["weight"] == 2.5 or reloaded["weight"] == "2.5"


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
