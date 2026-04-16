"""Dynamic properties — migrated from Katalon `API Coverage/ModulePlatform/DynamicProperties*`."""

import uuid

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Get registered object types for dynamic properties")
def test_dynamic_properties_get_types(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/dynamic/types"):
        types = rest_client.get(f"{backend_base_url}/api/platform/dynamic/types")

    with allure.step("Verify known types present"):
        assert isinstance(types, list)
        assert len(types) > 0
        assert any("Store" in t for t in types), f"Expected Store type, got: {types[:5]}..."


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Create and delete dynamic property")
def test_dynamic_property_create_delete(rest_client: RestClient, backend_base_url: str):
    base = f"{backend_base_url}/api/platform/dynamic/types"
    prop_name = f"QAProp_{uuid.uuid4().hex[:8]}"
    object_type = "VirtoCommerce.CustomerModule.Core.Model.Contact"

    with allure.step(f"POST dynamic property — name={prop_name}"):
        result = rest_client.post(
            f"{base}/{object_type}/properties",
            json={
                "name": prop_name,
                "valueType": "ShortText",
                "isArray": False,
                "isMultilingual": False,
                "isDictionary": False,
            },
        )

    with allure.step("Verify created"):
        assert result is not None
        prop_id = result.get("id")
        assert prop_id, "Property id missing"

    with allure.step("Cleanup — delete property"):
        rest_client.delete(
            f"{base}/{object_type}/properties",
            params={"propertyIds": [prop_id]},
        )


@pytest.mark.restapi
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Search dynamic properties for Contact type")
def test_dynamic_properties_search(rest_client: RestClient, backend_base_url: str):
    object_type = "VirtoCommerce.CustomerModule.Core.Model.Contact"

    with allure.step(f"POST /api/platform/dynamic/types/{object_type}/properties/search"):
        result = rest_client.post(
            f"{backend_base_url}/api/platform/dynamic/types/{object_type}/properties/search",
            json={"skip": 0, "take": 20},
        )

    with allure.step("Verify response"):
        assert result is not None
        assert "results" in result or "totalCount" in result
