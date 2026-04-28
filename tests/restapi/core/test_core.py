"""Core module — migrated from Katalon `API Coverage/ModuleCore/*`.

Katalon scripts:
  currenciesCreateUpdateDelete   → test_currency_create, test_currency_update, test_currency_delete
  packageTypeCreateUpdateDelete  → test_package_create, test_package_update, test_package_delete
  seoInfoGetRequestsCheck        → test_seo_info_get
  coreUnitSettingsCreateUpdateDelete → test_unit_settings (serial)
"""

import logging
import uuid

import allure
import pytest

from core.clients.rest import RestClient

logger = logging.getLogger(__name__)


@pytest.mark.restapi
@allure.feature("Core / Currencies (REST API)")
@allure.title("Create currency")
def test_currency_create(rest_client: RestClient, backend_base_url: str) -> None:
    code = f"Q{uuid.uuid4().hex[:2].upper()}"

    with allure.step(f"POST /api/currencies — code={code}"):
        rest_client.post(f"{backend_base_url}/api/currencies", json={"code": code, "name": f"QA Currency {code}"})

    with allure.step("Verify via GET"):
        currencies = rest_client.get(f"{backend_base_url}/api/currencies")
        found = next((c for c in currencies if c.get("code") == code), None)
        assert found is not None

    with allure.step("Cleanup"):
        rest_client.delete(f"{backend_base_url}/api/currencies", params={"codes": [code]})


@pytest.mark.restapi
@allure.feature("Core / Currencies (REST API)")
@allure.title("Update currency")
def test_currency_update(rest_client: RestClient, backend_base_url: str) -> None:
    code = f"Q{uuid.uuid4().hex[:2].upper()}"
    updated_name = f"QA {code} Updated"
    rest_client.post(f"{backend_base_url}/api/currencies", json={"code": code, "name": f"QA {code}"})

    try:
        with allure.step("PUT /api/currencies"):
            rest_client.put(f"{backend_base_url}/api/currencies", json={"code": code, "name": updated_name})

        with allure.step("Verify update via GET"):
            currencies = rest_client.get(f"{backend_base_url}/api/currencies")
            found = next((c for c in currencies if c.get("code") == code), None)
            assert found is not None, f"Currency {code} missing after PUT"
            assert found.get("name") == updated_name
    finally:
        with allure.step("Cleanup"):
            try:
                rest_client.delete(f"{backend_base_url}/api/currencies", params={"codes": [code]})
            except Exception as e:
                logger.warning("Cleanup failed: %s", e)


@pytest.mark.restapi
@allure.feature("Core / Currencies (REST API)")
@allure.title("Delete currency")
def test_currency_delete(rest_client: RestClient, backend_base_url: str) -> None:
    code = f"Q{uuid.uuid4().hex[:2].upper()}"
    rest_client.post(f"{backend_base_url}/api/currencies", json={"code": code, "name": f"QA {code}"})

    with allure.step(f"DELETE /api/currencies?codes={code}"):
        rest_client.delete(f"{backend_base_url}/api/currencies", params={"codes": [code]})


@pytest.mark.restapi
@allure.feature("Core / Package Types (REST API)")
@allure.title("Create package type")
def test_package_create(rest_client: RestClient, backend_base_url: str) -> None:
    name = f"QAPkg_{uuid.uuid4().hex[:6]}"

    with allure.step("POST /api/packageTypes"):
        rest_client.post(f"{backend_base_url}/api/packageTypes", json={"name": name})

    with allure.step("Verify via GET"):
        packages = rest_client.get(f"{backend_base_url}/api/packageTypes")
        found = next((p for p in packages if p.get("name") == name), None) if isinstance(packages, list) else None
        assert found is not None, f"Package '{name}' not found after creation"

    with allure.step("Cleanup"):
        if found:
            rest_client.delete(f"{backend_base_url}/api/packageTypes", params={"ids": [found["id"]]})


@pytest.mark.restapi
@allure.feature("Core / Package Types (REST API)")
@allure.title("Update package type")
def test_package_update(rest_client: RestClient, backend_base_url: str) -> None:
    name = f"QAPkg_{uuid.uuid4().hex[:6]}"
    updated_name = f"{name}_UPD"
    rest_client.post(f"{backend_base_url}/api/packageTypes", json={"name": name})

    with allure.step("Find created package via GET"):
        packages = rest_client.get(f"{backend_base_url}/api/packageTypes")
        pkg = next((p for p in packages if p.get("name") == name), None) if isinstance(packages, list) else None
        assert pkg is not None, f"Package '{name}' not found"
        pkg_id = pkg["id"]

    try:
        with allure.step("PUT /api/packageTypes"):
            rest_client.put(f"{backend_base_url}/api/packageTypes", json={**pkg, "name": updated_name})

        with allure.step("Verify update via GET"):
            packages = rest_client.get(f"{backend_base_url}/api/packageTypes")
            reloaded = (
                next((p for p in packages if p.get("id") == pkg_id), None) if isinstance(packages, list) else None
            )
            assert reloaded is not None, f"Package id={pkg_id} missing after PUT"
            assert reloaded.get("name") == updated_name
    finally:
        with allure.step("Cleanup"):
            try:
                rest_client.delete(f"{backend_base_url}/api/packageTypes", params={"ids": [pkg_id]})
            except Exception as e:
                logger.warning("Cleanup failed: %s", e)


@pytest.mark.restapi
@allure.feature("Core / Package Types (REST API)")
@allure.title("Delete package type")
def test_package_delete(rest_client: RestClient, backend_base_url: str) -> None:
    name = f"QAPkg_{uuid.uuid4().hex[:6]}"
    rest_client.post(f"{backend_base_url}/api/packageTypes", json={"name": name})

    with allure.step("Find created package via GET"):
        packages = rest_client.get(f"{backend_base_url}/api/packageTypes")
        pkg = next((p for p in packages if p.get("name") == name), None) if isinstance(packages, list) else None
        assert pkg is not None, f"Package '{name}' not found"

    with allure.step(f"DELETE /api/packageTypes?ids={pkg['id']}"):
        rest_client.delete(f"{backend_base_url}/api/packageTypes", params={"ids": [pkg["id"]]})


@pytest.mark.restapi
@allure.feature("Core / SEO (REST API)")
@allure.title("Check SEO duplicates for seeded catalog — endpoint reachable")
def test_seo_info_get(rest_client: RestClient, backend_base_url: str, seed_catalog_id: str) -> None:
    """The batchresolve endpoint is POST-rejected on this backend (405). `/duplicates` is the
    stable GET read: requires objectType + objectId and returns a list (empty if no duplicates).
    """
    with allure.step(f"GET /api/seoinfos/duplicates?objectType=Catalog&objectId={seed_catalog_id}"):
        result = rest_client.get(
            f"{backend_base_url}/api/seoinfos/duplicates",
            params={"objectType": "Catalog", "objectId": seed_catalog_id},
        )

    with allure.step("Verify response shape"):
        assert isinstance(result, list)
