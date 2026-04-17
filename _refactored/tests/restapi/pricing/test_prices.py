"""Price CRUD — migrated from Katalon `API Coverage/ModulePricing/price*`.

Katalon scripts:
  priceAddToTheProduct    → test_price_add_to_product
  priceUpdate             → test_price_update
  priceSearchGet          → test_price_search_get
  priceSearchPost         → test_price_search_post
  priceDeleteByPriceId    → test_price_delete_by_id
  pricesDeleteByProductId → test_price_delete_by_product
  pricesAddDeleteBulk     → test_price_add_delete_bulk
  pricesWidgetGet         → test_price_widget
"""

import allure
import pytest

from restapi.operations import PriceOperations


def _product_id(dataset: dict) -> str:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    return products[0]["id"]


def _catalog_id(dataset: dict) -> str:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    return products[0].get("catalogId", "")


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Add price to product")
def test_price_add_to_product(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    pid = _product_id(dataset)

    with allure.step("PUT /api/products/prices"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist["id"],
                    "productId": pid,
                    "list": 49.99,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step("Cleanup"):
        price_ops.delete_by_pricelist_and_product(pricelist["id"], pid)


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Update price via product endpoint")
def test_price_update(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    pid = _product_id(dataset)

    with allure.step("PUT /api/products/prices — initial"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist["id"],
                    "productId": pid,
                    "list": 10.00,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step("PUT /api/products/prices — update with new price"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist["id"],
                    "productId": pid,
                    "list": 25.00,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step("Cleanup"):
        price_ops.delete_by_pricelist_and_product(pricelist["id"], pid)


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Search prices — GET")
def test_price_search_get(make_pricelist, price_ops: PriceOperations) -> None:
    pricelist = make_pricelist()

    with allure.step(f"GET /api/catalog/products/prices/search?pricelistId={pricelist['id']}"):
        result = price_ops.search_get(pricelist_id=pricelist["id"])

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Search prices — POST")
def test_price_search_post(make_pricelist, price_ops: PriceOperations) -> None:
    pricelist = make_pricelist()

    with allure.step("POST /api/catalog/products/prices/search"):
        result = price_ops.search_post(pricelist_ids=[pricelist["id"]])

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Delete price by price id")
def test_price_delete_by_id(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    pid = _product_id(dataset)

    with allure.step("Add a price"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist["id"],
                    "productId": pid,
                    "list": 5.00,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step("Find price id via search"):
        result = price_ops.search_post(pricelist_ids=[pricelist["id"]])
        prices = result.get("results", []) if isinstance(result, dict) else result or []
        price_ids = [p["id"] for p in prices if p.get("id")]
        if price_ids:
            with allure.step(f"DELETE /api/pricing/products/prices?priceIds={price_ids[0]}"):
                price_ops.delete_by_price_id(price_ids[0])


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Delete prices by pricelist and product id")
def test_price_delete_by_product(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    pid = _product_id(dataset)

    with allure.step("Add a price"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist["id"],
                    "productId": pid,
                    "list": 7.50,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step(f"DELETE /api/pricing/pricelists/{pricelist['id']}/products/prices?productIds={pid}"):
        price_ops.delete_by_pricelist_and_product(pricelist["id"], pid)


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Add and delete prices in bulk")
def test_price_add_delete_bulk(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    products = dataset.get("products", [])
    if len(products) < 2:
        pytest.skip("Need at least 2 products in dataset")
    pid1 = products[0]["id"]
    pid2 = products[1]["id"]

    with allure.step("Add bulk prices"):
        price_ops.add_prices(
            [
                {"priceListId": pricelist["id"], "productId": pid1, "list": 1.00, "minQuantity": 1, "currency": "USD"},
                {"priceListId": pricelist["id"], "productId": pid2, "list": 2.00, "minQuantity": 1, "currency": "USD"},
            ]
        )

    with allure.step("Delete by pricelist+product"):
        price_ops.delete_by_pricelist_and_product(pricelist["id"], pid1, pid2)


@pytest.mark.restapi
@allure.feature("Pricing / Prices (REST API)")
@allure.title("Get prices widget")
def test_price_widget(price_ops: PriceOperations, dataset: dict) -> None:
    pid = _product_id(dataset)
    cat_id = _catalog_id(dataset)

    with allure.step(f"GET /api/products/{pid}/{cat_id}/pricesWidget"):
        result = price_ops.get_widget(pid, cat_id)

    with allure.step("Verify response"):
        assert result is not None
