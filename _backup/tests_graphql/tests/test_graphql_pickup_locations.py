import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_operations.pickup_locations.pickup_locations_operations import (
    PickupLocationsOperations,
)
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get all pickup locations for store (GraphQL)")
def test_get_pickup_locations(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    """Test retrieving all pickup locations for a store"""
    print(f"{os.linesep}Running test to get all pickup locations...", end=" ")

    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    result = pickup_locations_operations.get_pickup_locations(store_id=config["STORE_ID"])

    assert result["totalCount"] > 0, "No pickup locations found"
    assert len(result["items"]) > 0, "Pickup locations items list is empty"

    first_location = result["items"][0]
    assert "id" in first_location, "Pickup location missing id"
    assert "name" in first_location, "Pickup location missing name"
    assert "isActive" in first_location, "Pickup location missing isActive"


@pytest.mark.graphql
@allure.title("Get pickup locations with pagination (GraphQL)")
def test_get_pickup_locations_with_pagination(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    """Test pickup locations pagination"""
    print(f"{os.linesep}Running test for pickup locations pagination...", end=" ")

    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    first_page = pickup_locations_operations.get_pickup_locations(store_id=config["STORE_ID"], first=5)

    assert first_page["totalCount"] > 5, "Not enough pickup locations for pagination test"
    assert len(first_page["items"]) == 5, "First page should have 5 items"


@pytest.mark.graphql
@allure.title("Search pickup locations by keyword (GraphQL)")
def test_search_pickup_locations_by_keyword(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    """Test searching pickup locations by keyword"""
    print(f"{os.linesep}Running test to search pickup locations by keyword...", end=" ")

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    pickup_location_to_search = dataset["pickupLocations"][0]

    keyword = pickup_location_to_search["name"][:10]
    result = pickup_locations_operations.get_pickup_locations(store_id=config["STORE_ID"], keyword=keyword)
    print(keyword)

    assert result["totalCount"] >= 1, f"No pickup locations found for keyword: {keyword}"

    location_names = [loc["name"] for loc in result["items"]]
    assert any(
        pickup_location_to_search["name"] in name for name in location_names
    ), f"Expected location '{pickup_location_to_search['name']}' not found in results"


@pytest.mark.graphql
@allure.title("Verify pickup location has correct address (GraphQL)")
def test_pickup_location_address_structure(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    """Test that pickup locations have correct address structure"""
    print(
        f"{os.linesep}Running test to verify pickup location address structure...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    result = pickup_locations_operations.get_pickup_locations(store_id=config["STORE_ID"])

    assert result["totalCount"] > 0, "No pickup locations found"

    for location in result["items"]:
        if location["address"]:
            address = location["address"]
            assert "city" in address, f"Location {location['name']} missing city"
            assert "countryCode" in address, f"Location {location['name']} missing countryCode"
            assert "line1" in address, f"Location {location['name']} missing line1"


@pytest.mark.graphql
@allure.title("Update pickup location via WebAPI and verify via GraphQL")
def test_update_pickup_location(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
    webapi_client: WebAPISession,
):
    """Test updating pickup location via WebAPI and verifying via GraphQL"""
    print(f"{os.linesep}Running test to update pickup location...", end=" ")

    auth.authenticate(
        config["ADMIN_USERNAME"],
        config["ADMIN_PASSWORD"],
    )

    pickup_location_id = dataset["pickupLocations"][0]["id"]
    original_location = dataset["pickupLocations"][0]

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    initial_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=original_location["name"],
    )

    initial_location = None
    for loc in initial_result["items"]:
        if loc["id"] == pickup_location_id:
            initial_location = loc
            break

    assert initial_location is not None, f"Initial pickup location {pickup_location_id} not found via GraphQL"
    print(f"Initial location found: {initial_location['name']}")

    updated_name = original_location["name"] + " (Updated)"
    updated_description = original_location.get("description", "") + " (Updated)"
    updated_address = {
        "city": "San Francisco",
        "countryCode": "USA",
        "countryName": "United States",
        "line1": "1600 Holloway Drive",
        "postalCode": "10001",
        "regionId": "CA",
        "regionName": "California",
    }

    updated_location_data = {
        "id": pickup_location_id,
        "name": updated_name,
        "description": updated_description,
        "storeId": config["STORE_ID"],
        "isActive": original_location.get("isActive"),
        "geoLocation": original_location.get("geoLocation"),
        "workingHours": original_location.get("workingHours"),
        "contactPhone": original_location.get("contactPhone"),
        "contactEmail": original_location.get("contactEmail"),
        "fulfillmentCenterId": original_location.get("fulfillmentCenterId"),
        "address": updated_address,
    }

    webapi_client.post("/api/shipping/pickup-locations", data=updated_location_data)
    print(f"Updated pickup location via WebAPI")

    updated_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=updated_name,
    )

    assert updated_result["totalCount"] >= 1, f"Updated pickup location not found via GraphQL"

    found_location = None
    for loc in updated_result["items"]:
        if loc["id"] == pickup_location_id:
            found_location = loc
            break

    assert found_location is not None, f"Pickup location {pickup_location_id} not found in GraphQL results after update"
    assert (
        found_location["name"] == updated_name
    ), f"Name mismatch: expected '{updated_name}', got '{found_location['name']}'"
    assert (
        found_location["description"] == updated_description
    ), f"Description mismatch: expected '{updated_description}', got '{found_location['description']}'"
    assert (
        found_location["address"]["city"] == updated_address["city"]
    ), f"Address city mismatch: expected '{updated_address['city']}', got '{found_location['address']['city']}'"
    assert (
        found_location["address"]["countryCode"] == updated_address["countryCode"]
    ), f"Address country code mismatch: expected '{updated_address['countryCode']}', got '{found_location['address']['countryCode']}'"
    assert (
        found_location["address"]["countryName"] == updated_address["countryName"]
    ), f"Address country name mismatch: expected '{updated_address['countryName']}', got '{found_location['address']['countryName']}'"
    assert (
        found_location["address"]["line1"] == updated_address["line1"]
    ), f"Address line1 mismatch: expected '{updated_address['line1']}', got '{found_location['address']['line1']}'"
    assert (
        found_location["address"]["postalCode"] == updated_address["postalCode"]
    ), f"Address postal code mismatch: expected '{updated_address['postalCode']}', got '{found_location['address']['postalCode']}'"
    assert (
        found_location["address"]["regionId"] == updated_address["regionId"]
    ), f"Address region id mismatch: expected '{updated_address['regionId']}', got '{found_location['address']['regionId']}'"
    assert (
        found_location["address"]["regionName"] == updated_address["regionName"]
    ), f"Address region name mismatch: expected '{updated_address['regionName']}', got '{found_location['address']['regionName']}'"

    original_description = original_location.get("description", "")
    restore_location_data = {
        "id": pickup_location_id,
        "name": original_location["name"],
        "description": original_description,
        "storeId": original_location.get("storeId"),
        "isActive": original_location.get("isActive"),
        "geoLocation": original_location.get("geoLocation"),
        "workingHours": original_location.get("workingHours"),
        "contactPhone": original_location.get("contactPhone"),
        "contactEmail": original_location.get("contactEmail"),
        "fulfillmentCenterId": original_location.get("fulfillmentCenterId"),
        "address": original_location.get("address"),
    }
    webapi_client.post("/api/shipping/pickup-locations", data=restore_location_data)
    print(f"Restored original pickup location data")

    restored_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=original_location["name"],
    )

    restored_location = None
    for loc in restored_result["items"]:
        if loc["id"] == pickup_location_id:
            restored_location = loc
            break

    assert restored_location is not None, f"Restored pickup location not found via GraphQL"
    assert restored_location["name"] == original_location["name"], f"Restoration failed: name not restored"
    assert (
        restored_location.get("description", "") == original_description
    ), f"Description mismatch: expected '{original_description}', got '{restored_location.get('description', '')}'"
    assert restored_location.get("isActive") == original_location.get(
        "isActive"
    ), f"Is active mismatch: expected '{original_location.get('isActive')}', got '{restored_location.get('isActive')}'"

    original_addr = original_location.get("address", {})
    restored_addr = restored_location.get("address", {})
    assert restored_addr.get("city") == original_addr.get("city"), f"Address city mismatch"
    assert restored_addr.get("countryCode") == original_addr.get("countryCode"), f"Address country code mismatch"
    assert restored_addr.get("line1") == original_addr.get("line1"), f"Address line1 mismatch"


@pytest.mark.graphql
@allure.title("Set inactive pickup location via WebAPI and verify via GraphQL")
def test_set_inactive_pickup_location(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
    webapi_client: WebAPISession,
):
    """Test setting inactive pickup location via WebAPI and verifying via GraphQL"""
    print(f"{os.linesep}Running test to set inactive pickup location...", end=" ")

    auth.authenticate(
        config["ADMIN_USERNAME"],
        config["ADMIN_PASSWORD"],
    )

    pickup_location_id = dataset["pickupLocations"][2]["id"]
    original_location = dataset["pickupLocations"][2]

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    initial_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=original_location["name"],
    )

    initial_location = None
    for loc in initial_result["items"]:
        if loc["id"] == pickup_location_id:
            initial_location = loc
            break

    if initial_location is None:
        restore_data = {
            "id": pickup_location_id,
            "isActive": True,
            "name": original_location["name"],
            "description": original_location.get("description", ""),
            "storeId": original_location.get("storeId"),
            "geoLocation": original_location.get("geoLocation"),
            "workingHours": original_location.get("workingHours"),
            "contactPhone": original_location.get("contactPhone"),
            "contactEmail": original_location.get("contactEmail"),
            "fulfillmentCenterId": original_location.get("fulfillmentCenterId"),
            "address": original_location.get("address"),
        }
        webapi_client.post("/api/shipping/pickup-locations", data=restore_data)

        initial_result = pickup_locations_operations.get_pickup_locations(
            store_id=config["STORE_ID"],
            keyword=original_location["name"],
        )
        for loc in initial_result["items"]:
            if loc["id"] == pickup_location_id:
                initial_location = loc
                break

    assert (
        initial_location is not None
    ), f"Initial pickup location {pickup_location_id} not found via GraphQL even after restore attempt"
    print(f"Initial location found: {initial_location['name']}")

    updated_location_data = {
        "id": pickup_location_id,
        "isActive": False,
        "name": original_location["name"],
        "description": original_location.get("description", ""),
        "storeId": original_location.get("storeId"),
        "geoLocation": original_location.get("geoLocation"),
        "workingHours": original_location.get("workingHours"),
        "contactPhone": original_location.get("contactPhone"),
        "contactEmail": original_location.get("contactEmail"),
        "fulfillmentCenterId": original_location.get("fulfillmentCenterId"),
        "address": original_location.get("address"),
    }
    webapi_client.post("/api/shipping/pickup-locations", data=updated_location_data)
    print(f"Set inactive pickup location via WebAPI")

    updated_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=original_location["name"],
    )

    assert updated_result["totalCount"] == 0, f"Inactive pickup location found via GraphQL"
    print(f"Inactive pickup location not found via GraphQL")

    restore_location_data = {
        "id": pickup_location_id,
        "isActive": original_location.get("isActive"),
        "name": original_location["name"],
        "description": original_location.get("description", ""),
        "storeId": original_location.get("storeId"),
        "geoLocation": original_location.get("geoLocation"),
        "workingHours": original_location.get("workingHours"),
        "contactPhone": original_location.get("contactPhone"),
        "contactEmail": original_location.get("contactEmail"),
        "fulfillmentCenterId": original_location.get("fulfillmentCenterId"),
        "address": original_location.get("address"),
    }
    webapi_client.post("/api/shipping/pickup-locations", data=restore_location_data)
    print(f"Restored pickup location via WebAPI")

    restored_result = pickup_locations_operations.get_pickup_locations(
        store_id=config["STORE_ID"],
        keyword=original_location["name"],
    )

    assert restored_result["totalCount"] >= 1, f"Restored pickup location not found via GraphQL"
    assert (
        restored_result["items"][0]["isActive"] == original_location["isActive"]
    ), f"Is active mismatch: expected '{original_location['isActive']}', got '{restored_result['items'][0]['isActive']}'"
