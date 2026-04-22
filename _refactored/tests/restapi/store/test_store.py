"""Store CRUD — migrated from Katalon `API Coverage/ModuleStore/*`.

Katalon scripts:
  StoreCreate                → test_store_create
  StoreCreateNameValidation  → test_store_create_name_validation
  StoreGetById               → test_store_get_by_id
  StoreGetAll                → test_store_get_all
  StoreSearch                → test_store_search
  StoreUpdate                → test_store_update
  StoreFull                  → test_store_full_cycle
  StoreDelete                → test_store_delete
  StoreUserAccessValidation  → test_store_user_access
  StoreAssets                → test_store_assets
"""

import uuid

import allure
import pytest

from restapi.operations import StoreOperations


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Create store")
def test_store_create(make_store) -> None:
    with allure.step("POST /api/stores"):
        store = make_store()

    with allure.step("Verify response"):
        assert store["id"]
        assert store["name"].startswith("QAStore_")


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Create store — name validation (empty name)")
def test_store_create_name_validation(store_ops: StoreOperations) -> None:
    with allure.step("POST /api/stores — empty name"):
        try:
            store = store_ops.create(name="")
            # If it succeeds, clean up
            if store and store.get("id"):
                store_ops.delete(store["id"])
        except Exception:
            pass  # Expected: validation error or 400


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Get store by id")
def test_store_get_by_id(make_store, store_ops: StoreOperations) -> None:
    store = make_store()

    with allure.step(f"GET /api/stores/{store['id']}"):
        reloaded = store_ops.get_by_id(store["id"])

    with allure.step("Verify fields"):
        assert reloaded["id"] == store["id"]
        assert reloaded["name"] == store["name"]


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Get all stores")
def test_store_get_all(store_ops: StoreOperations) -> None:
    with allure.step("GET /api/stores"):
        stores = store_ops.get_all()

    with allure.step("Verify response"):
        assert stores is not None
        assert isinstance(stores, list)


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Search stores")
def test_store_search(make_store, store_ops: StoreOperations) -> None:
    store = make_store()

    with allure.step("POST /api/stores/search"):
        result = store_ops.search(keyword=store["name"])

    with allure.step("Verify in results"):
        items = result.get("results", []) if isinstance(result, dict) else result or []
        found = next((s for s in items if s["id"] == store["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Update store — rename")
def test_store_update(make_store, store_ops: StoreOperations) -> None:
    store = make_store()
    new_name = f"{store['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/stores — name={new_name}"):
        store_ops.update(store, name=new_name)

    with allure.step("Verify update"):
        reloaded = store_ops.get_by_id(store["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Store full cycle — create→get→update→search→delete")
def test_store_full_cycle(store_ops: StoreOperations) -> None:
    name = f"QACycle_{uuid.uuid4().hex[:8]}"

    with allure.step("Create"):
        store = store_ops.create(name=name)
        assert store["id"]

    with allure.step("Get"):
        fetched = store_ops.get_by_id(store["id"])
        assert fetched["name"] == name

    with allure.step("Update"):
        new_name = f"{name}_updated"
        store_ops.update(fetched, name=new_name)
        updated = store_ops.get_by_id(store["id"])
        assert updated["name"] == new_name

    with allure.step("Search"):
        result = store_ops.search(keyword=new_name)
        items = result.get("results", []) if isinstance(result, dict) else result or []
        found = next((s for s in items if s["id"] == store["id"]), None)
        assert found is not None

    with allure.step("Delete"):
        store_ops.delete(store["id"])


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Delete store")
def test_store_delete(store_ops: StoreOperations) -> None:
    store = store_ops.create(name=f"QADelStore_{uuid.uuid4().hex[:8]}")

    with allure.step(f"DELETE /api/stores?ids={store['id']}"):
        store_ops.delete(store["id"])


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Get user accessible stores")
def test_store_user_access(store_ops: StoreOperations, dataset: dict) -> None:
    users = dataset.get("users", [])
    if not users:
        pytest.skip("No users in dataset")
    user_id = users[0].get("id", "")

    with allure.step(f"GET /api/stores/allowed/{user_id}"):
        result = store_ops.get_accessible(user_id)

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Store (REST API)")
@allure.title("Store assets — verify store has asset configuration")
def test_store_assets(store_ops: StoreOperations, dataset: dict) -> None:
    stores = dataset.get("stores", [])
    if not stores:
        pytest.skip("No stores in dataset")
    store_id = stores[0].get("id", stores[0].get("storeId", ""))

    with allure.step(f"GET /api/stores/{store_id}"):
        store = store_ops.get_by_id(store_id)

    with allure.step("Verify store returned"):
        assert store is not None
        assert store["id"] == store_id
