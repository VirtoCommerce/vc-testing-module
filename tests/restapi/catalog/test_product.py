"""Product CRUD — migrated from Katalon `API Coverage/ModuleCatalog/product*`."""

import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from restapi.operations import ProductOperations, SettingsOperations


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Create product")
def test_product_create(make_product) -> None:
    with allure.step("POST /api/catalog/products"):
        product = make_product()

    with allure.step("Verify response"):
        assert product.id, "Product id missing"
        assert product.name.startswith("QAProduct_")
        assert product.code.startswith("QA-SKU-")
        assert product.catalog_id
        assert product.category_id


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Update product — rename and change dimensions")
def test_product_update(make_product, product_ops: ProductOperations) -> None:
    product = make_product()
    new_name = f"{product.name}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"POST /api/catalog/products — rename to {new_name}, weight=2.5"):
        product_ops.update(product, name=new_name, weight="2.5")

    with allure.step("Verify update via GET"):
        reloaded = product_ops.get_by_id(product.id)
        assert reloaded.name == new_name
        weight = reloaded.model_extra.get("weight") if reloaded.model_extra else None
        assert weight == 2.5 or weight == "2.5"


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Get product by id")
def test_product_get_by_id(make_product, product_ops: ProductOperations) -> None:
    product = make_product()

    with allure.step(f"GET /api/catalog/products?ids={product.id}"):
        reloaded = product_ops.get_by_id(product.id)

    with allure.step("Verify fields match"):
        assert reloaded.id == product.id
        assert reloaded.name == product.name
        assert reloaded.code == product.code


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Delete product")
def test_product_delete(make_product, product_ops: ProductOperations) -> None:
    product = make_product()

    with allure.step(f"POST /api/catalog/listentries/delete — objectIds=[{product.id}]"):
        product_ops.delete(product.id)

    with allure.step("Verify product no longer returned by GET"):
        try:
            results = product_ops.get_by_ids([product.id])
        except HTTPError as e:
            assert e.response.status_code in (404, 204)
        else:
            ids = [r.id for r in (results or [])]
            assert product.id not in ids


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Update product images")
def test_product_update_image(make_product, product_ops: ProductOperations) -> None:
    product = make_product()
    image = {
        "name": "qa-image.svg",
        "url": "/qa-images/qa-image.svg",
        "relativeUrl": "/qa-images/qa-image.svg",
        "size": 6129,
        "contentType": "image/svg+xml",
        "type": "blob",
        "isImage": True,
        "sortOrder": 1,
        "group": "images",
        "createdDate": "0001-01-01T00:00:00Z",
    }

    with allure.step("POST /api/catalog/products — add image"):
        product_ops.update(product, images=[image])

    with allure.step("Verify image persisted"):
        reloaded = product_ops.get_by_id(product.id)
        images = (reloaded.model_extra or {}).get("images") or []
        urls = [img.get("url") or "" for img in images]
        assert any(image["url"] in u for u in urls), f"Expected url ending with {image['url']}, got {urls}"


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Create/update product via raw body (clone flow)")
def test_product_create_update_with_body(make_product, product_ops: ProductOperations) -> None:
    product = make_product()

    with allure.step(f"GET /api/catalog/products/{product.id}/clone"):
        clone_body = product_ops.get_clone(product.id)

    cloned_code = f"{clone_body['code']}-C{uuid.uuid4().hex[:4]}"
    clone_body["code"] = cloned_code
    clone_body.pop("id", None)

    with allure.step("POST /api/catalog/products — persist clone"):
        created = product_ops.create_or_update_with_body(clone_body)

    try:
        with allure.step("Verify cloned product id"):
            assert created.id
            assert created.id != product.id
    finally:
        with allure.step("Cleanup cloned product"):
            try:
                product_ops.delete(created.id)
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Get product by non-existent id — expect empty result or 404")
def test_product_get_not_found(product_ops: ProductOperations) -> None:
    bogus_id = f"qa-missing-{uuid.uuid4().hex}"

    with allure.step(f"GET /api/catalog/products?ids={bogus_id}"):
        try:
            results = product_ops.get_by_ids([bogus_id])
        except HTTPError as exc:
            assert exc.response.status_code == 404
        else:
            ids = [r.id for r in (results or [])]
            assert bogus_id not in ids


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Get product clone body")
def test_product_get_clone_body(make_product, product_ops: ProductOperations) -> None:
    product = make_product()

    with allure.step(f"GET /api/catalog/products/{product.id}/clone"):
        clone = product_ops.get_clone(product.id)

    with allure.step("Verify clone shape"):
        assert clone.get("name") == product.name
        assert clone.get("catalogId") == product.catalog_id


@pytest.mark.restapi
@allure.feature("Catalog / Products (REST API)")
@allure.title("Move product to another catalog")
def test_product_move_to_catalog(make_product, make_catalog, product_ops: ProductOperations) -> None:
    product = make_product()
    target_catalog = make_catalog()

    with allure.step(f"POST /api/catalog/listentries/move — to catalog {target_catalog.id}"):
        product_ops.move(
            target_catalog_id=target_catalog.id,
            list_entries=[
                {
                    "id": product.id,
                    "type": "product",
                    "name": product.name,
                    "code": product.code,
                    "catalogId": product.catalog_id,
                    "isActive": True,
                }
            ],
        )

    with allure.step("Verify product now references target catalog"):
        reloaded = product_ops.get_by_id(product.id)
        assert reloaded.catalog_id == target_catalog.id


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog / Products (REST API)")
@allure.title("Editorial review types — add, rename, remove")
def test_product_description_types(rest_client, backend_base_url) -> None:
    setting_name = "Catalog.EditorialReviewTypes"
    settings_ops = SettingsOperations(rest_client, backend_base_url)

    def set_types(values: list[str]) -> None:
        current = settings_ops.get_by_name(setting_name)
        current["allowedValues"] = values
        settings_ops.update([current])

    with allure.step("Read current review types"):
        original = settings_ops.get_by_name(setting_name)
        original_values = list(original.get("allowedValues") or [])
        assert original["name"] == setting_name

    try:
        with allure.step("Add new type 'TEST'"):
            set_types(original_values + ["TEST"])
            after_add = settings_ops.get_by_name(setting_name)
            assert "TEST" in (after_add.get("allowedValues") or [])

        with allure.step("Rename 'TEST' -> 'TESTUPD'"):
            set_types(original_values + ["TESTUPD"])
            after_rename = settings_ops.get_by_name(setting_name)
            assert "TESTUPD" in (after_rename.get("allowedValues") or [])
            assert "TEST" not in (after_rename.get("allowedValues") or [])
    finally:
        with allure.step("Restore original review types"):
            set_types(original_values)
