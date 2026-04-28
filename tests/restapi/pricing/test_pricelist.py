"""Pricelist CRUD — migrated from Katalon `API Coverage/ModulePricing/pricelist*`.

Katalon scripts:
  pricelistCreate          → test_pricelist_create
  pricelistUpdate          → test_pricelist_update
  pricelistGet             → test_pricelist_search (keyword search)
  pricelistGetByPricelistId → test_pricelist_get_by_id
  pricelistsGetAll         → test_pricelist_get_all
  pricelistDelete          → test_pricelist_delete
  pricelistProductsAdd     → test_pricelist_add_products
"""

import uuid

import allure
import pytest

from restapi.operations import PricelistOperations, PriceOperations


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Create pricelist")
def test_pricelist_create(make_pricelist) -> None:
    with allure.step("POST /api/pricing/pricelists"):
        pricelist = make_pricelist()

    with allure.step("Verify response"):
        assert pricelist.id
        assert pricelist.name.startswith("QAPricelist_")
        assert pricelist.currency == "USD"


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Update pricelist — rename")
def test_pricelist_update(make_pricelist, pricelist_ops: PricelistOperations) -> None:
    pricelist = make_pricelist()
    new_name = f"{pricelist.name}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/pricing/pricelists — name={new_name}"):
        pricelist_ops.update(pricelist, name=new_name)

    with allure.step("Verify update"):
        reloaded = pricelist_ops.get_by_id(pricelist.id)
        assert reloaded.name == new_name


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Search pricelists by keyword")
def test_pricelist_search(make_pricelist, pricelist_ops: PricelistOperations) -> None:
    pricelist = make_pricelist()

    with allure.step(f"GET /api/pricing/pricelists?keyword={pricelist.name}"):
        result = pricelist_ops.search(keyword=pricelist.name)

    with allure.step("Verify in results"):
        items = result if isinstance(result, list) else result.get("results", [])
        found = next((r for r in items if r["id"] == pricelist.id), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Get pricelist by id")
def test_pricelist_get_by_id(make_pricelist, pricelist_ops: PricelistOperations) -> None:
    pricelist = make_pricelist()

    with allure.step(f"GET /api/pricing/pricelists/{pricelist.id}"):
        reloaded = pricelist_ops.get_by_id(pricelist.id)

    with allure.step("Verify fields"):
        assert reloaded.id == pricelist.id
        assert reloaded.name == pricelist.name


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Get all pricelists")
def test_pricelist_get_all(pricelist_ops: PricelistOperations) -> None:
    with allure.step("GET /api/pricing/pricelists"):
        result = pricelist_ops.search()

    with allure.step("Verify response shape"):
        items = result if isinstance(result, list) else result.get("results", [])
        assert isinstance(items, list)


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Delete pricelist")
def test_pricelist_delete(pricelist_ops: PricelistOperations) -> None:
    name = f"QADelPL_{uuid.uuid4().hex[:8]}"
    pricelist = pricelist_ops.create(name=name)

    with allure.step(f"DELETE /api/pricing/pricelists?ids={pricelist.id}"):
        pricelist_ops.delete(pricelist.id)

    with allure.step("Verify deleted"):
        result = pricelist_ops.search(keyword=name)
        items = result if isinstance(result, list) else result.get("results", [])
        ids = [r["id"] for r in items]
        assert pricelist.id not in ids


@pytest.mark.restapi
@allure.feature("Pricing / Pricelists (REST API)")
@allure.title("Add products to pricelist")
def test_pricelist_add_products(make_pricelist, price_ops: PriceOperations, dataset: dict) -> None:
    pricelist = make_pricelist()
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    pid = products[0]["id"]

    with allure.step("PUT /api/products/prices — add price entry"):
        price_ops.add_prices(
            [
                {
                    "priceListId": pricelist.id,
                    "productId": pid,
                    "list": 99.99,
                    "minQuantity": 1,
                    "currency": "USD",
                }
            ]
        )

    with allure.step("Cleanup"):
        price_ops.delete_by_pricelist_and_product(pricelist.id, pid)
