"""Dynamic properties — migrated from Katalon `API Coverage/ModulePlatform/DynamicProperties/*`.

Real endpoints (from Katalon Object Repository):
  - GET  /api/platform/dynamic/types
  - POST /api/platform/dynamic/properties       (create — objectType in body)
  - POST /api/platform/dynamic/properties/search (search — objectType in body)
  - DELETE /api/platform/dynamic/properties?propertyIds=...
"""

import uuid

import allure
import pytest

from core.clients.rest import RestClient

DYNAMIC_PROPERTY_OBJECT_TYPES = [
    "VirtoCommerce.CartModule.Core.Model.LineItem",
    "VirtoCommerce.CartModule.Core.Model.Payment",
    "VirtoCommerce.CartModule.Core.Model.Shipment",
    "VirtoCommerce.CartModule.Core.Model.ShoppingCart",
    "VirtoCommerce.ContentModule.Core.Model.FrontMatterHeaders",
    "VirtoCommerce.CustomerModule.Core.Model.Contact",
    "VirtoCommerce.CustomerModule.Core.Model.Employee",
    "VirtoCommerce.CustomerModule.Core.Model.Organization",
    "VirtoCommerce.CustomerModule.Core.Model.Vendor",
    "VirtoCommerce.MarketingModule.Core.Model.DynamicContentItem",
    "VirtoCommerce.OrdersModule.Core.Model.CustomerOrder",
    "VirtoCommerce.OrdersModule.Core.Model.LineItem",
    "VirtoCommerce.OrdersModule.Core.Model.PaymentIn",
    "VirtoCommerce.OrdersModule.Core.Model.Shipment",
    "VirtoCommerce.QuoteModule.Core.Model.QuoteRequest",
    "VirtoCommerce.StoreModule.Core.Model.Store",
]


def _short_type(object_type: str) -> str:
    return object_type.rsplit(".", 1)[-1]


@pytest.mark.restapi
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Get registered object types for dynamic properties")
def test_dynamic_properties_get_types(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/dynamic/types"):
        types = rest_client.get(f"{backend_base_url}/api/platform/dynamic/types")

    with allure.step("Verify known types present"):
        assert isinstance(types, list)
        assert len(types) > 0
        assert any("Store" in t for t in types)


@pytest.mark.restapi
@pytest.mark.serial
@pytest.mark.parametrize(
    "object_type", DYNAMIC_PROPERTY_OBJECT_TYPES, ids=[_short_type(t) for t in DYNAMIC_PROPERTY_OBJECT_TYPES]
)
@allure.feature("Platform / Dynamic Properties (REST API)")
def test_dynamic_property_create_verify_delete(rest_client: RestClient, backend_base_url: str, object_type: str):
    allure.dynamic.title(f"Create + delete dynamic property — {_short_type(object_type)}")
    base = f"{backend_base_url}/api/platform/dynamic"
    prop_name = f"QAProp_{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/platform/dynamic/properties — {_short_type(object_type)}"):
        result = rest_client.post(
            f"{base}/properties",
            json={"objectType": object_type, "name": prop_name, "valueType": "ShortText"},
        )
        assert result is not None
        assert result.get("name") == prop_name
        prop_id = result["id"]

    with allure.step("Verify property in search"):
        search = rest_client.post(
            f"{base}/properties/search",
            json={"objectType": object_type, "skip": 0, "take": 100},
        )
        names = [p.get("name") for p in search.get("results", [])]
        assert prop_name in names, f"Property {prop_name} not found: {names[:10]}..."

    with allure.step("Delete property"):
        rest_client.delete(f"{base}/properties", params={"propertyIds": [prop_id]})


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Create dictionary dynamic property on Contact")
def test_dynamic_property_create_dictionary(rest_client: RestClient, backend_base_url: str):
    base = f"{backend_base_url}/api/platform/dynamic"
    object_type = "VirtoCommerce.CustomerModule.Core.Model.Contact"
    prop_name = f"QADictProp_{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST dictionary property name={prop_name}"):
        result = rest_client.post(
            f"{base}/properties",
            json={"objectType": object_type, "name": prop_name, "valueType": "ShortText", "isDictionary": True},
        )
        assert result is not None
        prop_id = result["id"]

    with allure.step("Verify isDictionary flag"):
        assert result.get("isDictionary") is True

    with allure.step("Cleanup"):
        rest_client.delete(f"{base}/properties", params={"propertyIds": [prop_id]})


@pytest.mark.restapi
@pytest.mark.serial
@pytest.mark.parametrize(
    "value_type,is_array,is_multilingual",
    [
        ("ShortText", False, False),
        ("ShortText", True, False),
        ("ShortText", False, True),
        ("LongText", False, False),
        ("Integer", False, False),
        ("Decimal", False, False),
        ("DateTime", False, False),
        ("Boolean", False, False),
        ("Html", False, False),
    ],
    ids=lambda p: str(p) if isinstance(p, str) else None,
)
@allure.feature("Platform / Dynamic Properties (REST API)")
def test_dynamic_property_value_types(
    rest_client: RestClient, backend_base_url: str, value_type: str, is_array: bool, is_multilingual: bool
):
    allure.dynamic.title(f"Create property — {value_type} array={is_array} multilingual={is_multilingual}")
    base = f"{backend_base_url}/api/platform/dynamic"
    object_type = "VirtoCommerce.CustomerModule.Core.Model.Contact"
    prop_name = f"QA_{value_type}_{uuid.uuid4().hex[:6]}"

    with allure.step(f"POST property {prop_name}"):
        result = rest_client.post(
            f"{base}/properties",
            json={
                "objectType": object_type,
                "name": prop_name,
                "valueType": value_type,
                "isArray": is_array,
                "isMultilingual": is_multilingual,
                "isDictionary": False,
            },
        )
        assert result is not None
        assert result.get("name") == prop_name
        prop_id = result["id"]

    with allure.step("Cleanup"):
        rest_client.delete(f"{base}/properties", params={"propertyIds": [prop_id]})


@pytest.mark.restapi
@allure.feature("Platform / Dynamic Properties (REST API)")
@allure.title("Search dynamic properties for Contact type")
def test_dynamic_properties_search(rest_client: RestClient, backend_base_url: str):
    object_type = "VirtoCommerce.CustomerModule.Core.Model.Contact"

    with allure.step("POST /api/platform/dynamic/properties/search"):
        result = rest_client.post(
            f"{backend_base_url}/api/platform/dynamic/properties/search",
            json={"objectType": object_type, "skip": 0, "take": 20},
        )

    with allure.step("Verify response"):
        assert result is not None
        assert "results" in result or "totalCount" in result
