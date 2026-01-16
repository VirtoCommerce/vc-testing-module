import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.pickup_locations.pickup_locations_operations import (
    PickupLocationsOperations,
)
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get product pickup locations - product in main FFC (GraphQL)")
def test_product_pickup_locations_main_ffc(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for a product available in main FFC (Illinois)"""
    print(
        f"{os.linesep}Running test to get product pickup locations (main FFC)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    # Product2 - Main_1 stock is in Illinois FFC only
    product_id = "product-acme-product2-main1-stock"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found for product"

    availability_types = [loc.get("availabilityType") for loc in result["items"]]
    assert any(
        avail in ["Today", "Transfer", "GlobalTransfer"] for avail in availability_types
    ), "No valid availability type found"

    # Verify locations with Illinois FFC as main should have "Today" availability
    locations_with_today = [
        loc for loc in result["items"] if loc.get("availabilityType") == "Today"
    ]
    assert len(locations_with_today) > 0, "No locations with Today availability found"


@pytest.mark.graphql
@allure.title("Get product pickup locations - product in Ohio FFC (GraphQL)")
def test_product_pickup_locations_ohio_ffc(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for a product available in Ohio FFC"""
    print(
        f"{os.linesep}Running test to get product pickup locations (Ohio FFC)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    # Product2 - Main_2 stock is in Ohio FFC only
    product_id = "product-acme-product2-main2-stock"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found for product"

    # Locations with Ohio FFC as main should have direct availabity
    for location in result["items"]:
        if location.get("availabilityType") == "Today":
            assert (
                location.get("availableQuantity", 0) > 0
            ), f"Location {location['name']} has Today availability but no stock"


@pytest.mark.graphql
@allure.title("Get product pickup locations - product in multiple FFCs (GraphQL)")
def test_product_pickup_locations_multi_ffc(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for a product available in multiple FFCs (Illinois + Ohio)"""
    print(
        f"{os.linesep}Running test to get product pickup locations (multi-FFC)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    product_id = "product-acme-product4-main-transfer"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found for multi-FFC product"

    locations_with_today = [
        loc for loc in result["items"] if loc.get("availabilityType") == "Today"

    ]  

    assert (
        len(locations_with_today) > 1
    ), f"Multi-FFC product should have Today availability at multiple locations, found {len(locations_with_today)}"

    for location in locations_with_today:
        assert (
            location.get("availableQuantity", 0) > 0
        ), f"Location {location['name']} has Today availability but no stock"

    


@pytest.mark.graphql
@allure.title("Get product pickup locations - product with zero stock (GraphQL)")
def test_product_pickup_locations_zero_stock(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for a product with zero stock in all FFCs"""
    print(
        f"{os.linesep}Running test to get product pickup locations (zero stock)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    # Product6 has zero stock
    product_id = "product-acme-product6-track-inventory-true-stock-0"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    # All locations should have zero available quantity
    for location in result["items"]:
        available_qty = location.get("availableQuantity", 0)
        assert (
            available_qty == 0
        ), f"Location {location['name']} should have 0 stock, got {available_qty}"


@pytest.mark.graphql
@allure.title("Get product pickup locations - European product Berlin+Billund (GraphQL)")
def test_product_pickup_locations_european_berlin_billund(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for a product only available in Berlin and Billund FFCs"""
    print(
        f"{os.linesep}Running test to get product pickup locations (European Berlin+Billund)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    # Product7 is only in Berlin and Billund FFCs
    product_id = "product-acme-product7-berlin"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found for European product"

    # Find European locations with availability
    european_locations = [
        loc
        for loc in result["items"]
        if loc.get("address", {}).get("countryCode") in ["DEU", "DNK"]
    ]

    european_with_stock = [
        loc for loc in european_locations if loc.get("availableQuantity", 0) > 0
    ]

    assert (
        len(european_with_stock) > 0
    ), "No European locations have stock for this product"

    print(f"Found {len(european_with_stock)} European locations with stock")


@pytest.mark.graphql
@allure.title("Get product pickup locations - product in 3 FFCs (GraphQL)")
def test_product_pickup_locations_three_ffcs(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for Product5 available in Berlin, Billund, and Morrisville NC FFCs"""
    print(
        f"{os.linesep}Running test to get product pickup locations (3 FFCs)...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    product_id = "product-acme-product5-transfer123"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found"

    locations_with_stock = [
        loc for loc in result["items"] if loc.get("availableQuantity", 0) > 0
    ]

    assert len(locations_with_stock) > 3, "Product in 3 FFCs should be available at many locations"

    us_locations = [
        loc
        for loc in locations_with_stock
        if loc.get("address", {}).get("countryCode") == "USA"
    ]
    eu_locations = [
        loc
        for loc in locations_with_stock
        if loc.get("address", {}).get("countryCode") in ["DEU", "DNK"]
    ]

    print(f"US locations with stock: {len(us_locations)}, EU locations with stock: {len(eu_locations)}")


@pytest.mark.graphql
@allure.title("Get product pickup locations with pagination (GraphQL)")
def test_product_pickup_locations_pagination(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test product pickup locations pagination"""
    print(
        f"{os.linesep}Running test for product pickup locations pagination...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    # Use a product available in many locations
    product_id = "product-acme-product3-transfer"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    # Get first page with 5 items
    first_page = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
        first=5,
    )

    assert first_page["totalCount"] > 5, "Not enough pickup locations for pagination test"
    assert len(first_page["items"]) == 5, f"First page should have 5 items, got {len(first_page['items'])}"


@pytest.mark.graphql
@allure.title("Get product pickup locations - verify availability types (GraphQL)")
def test_product_pickup_locations_availability_types(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that product pickup locations return correct availability types"""
    print(
        f"{os.linesep}Running test to verify availability types...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]
    
    product_id = "product-acme-product4-main-transfer"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    availability_types = set()
    for location in result["items"]:
        if location.get("availabilityType"):
            availability_types.add(location["availabilityType"])

    print(f"Found availability types: {availability_types}")

    valid_types = {"Today", "Transfer", "GlobalTransfer", None}
    for avail_type in availability_types:
        assert (
            avail_type in valid_types
        ), f"Invalid availability type: {avail_type}"


@pytest.mark.graphql
@allure.title("Get product pickup locations - verify address structure (GraphQL)")
def test_product_pickup_locations_address_structure(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that product pickup locations have correct address structure"""
    print(
        f"{os.linesep}Running test to verify address structure...",
        end=" ",
    )

    pickup_locations_operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]

    product_id = "product-acme-product3-transfer"
    product = next(
        (p for p in dataset["products"] if p["id"] == product_id),
        None,
    )

    if product is None:
        pytest.skip(f"Test product {product_id} not found in dataset")

    result = pickup_locations_operations.get_product_pickup_locations(
        product_id=product["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    for location in result["items"]:
        assert "id" in location, "Location missing id"
        assert "name" in location, "Location missing name"
        assert "isActive" in location, "Location missing isActive"

        if location.get("address"):
            address = location["address"]
            assert "city" in address, f"Location {location['name']} missing city"
            assert "countryCode" in address, f"Location {location['name']} missing countryCode"
            assert "line1" in address, f"Location {location['name']} missing line1"
