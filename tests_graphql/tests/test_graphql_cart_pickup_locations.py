import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.pickup_locations.pickup_locations_operations import (
    PickupLocationsOperations,
)
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get cart pickup locations - product with transfer required (GraphQL)")
def test_get_cart_pickup_locations_transfer_required(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for cart with product requiring transfer"""
    print(
        f"{os.linesep}Running test to get cart pickup locations (transfer required)...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    product_transfer = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product5-transfer-b2b"),
        None,
    )

    if product_transfer is None:
        pytest.skip("Test product not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_transfer["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    transfer_locations = [
        loc
        for loc in result["items"]
        if loc.get("availabilityType") in ["Transfer", "GlobalTransfer"]
    ]

    print(f"Found {len(transfer_locations)} locations with transfer availability")

    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )

@pytest.mark.graphql
@allure.title("Get cart pickup locations - multiple products (GraphQL)")
def test_get_cart_pickup_locations_multiple_products(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test getting pickup locations for cart with multiple products"""
    print(
        f"{os.linesep}Running test to get cart pickup locations (multiple products)...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    product1 = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product2-main1-stock"),
        None,
    )

    product2 = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product5-transfer-b2b"),
        None,
    )

    if product1 is None or product2 is None:
        pytest.skip("Test products not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product1["id"],
            "quantity": 1,
        }
    )

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
            "productId": product2["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert result["totalCount"] > 0, "No pickup locations found for cart with multiple products"
    assert len(result['items']) > 0, "No pickup location items returned"    
 
    valid_availability_types = {"Today", "Transfer", "GlobalTransfer"}
    transfer_locations = []
    for item in result['items']:
        assert item['availabilityType'] in valid_availability_types, \
            f"Invalid availability type: {item['availabilityType']}"
        if item['availabilityType'] in ["Transfer", "GlobalTransfer"]:
            transfer_locations.append(item)
    
    print(f"Found {len(transfer_locations)} locations with Transfer availability out of {len(result['items'])} total")

    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )


@pytest.mark.graphql
@allure.title("Cart pickup locations - verify Today availability type (GraphQL)")
def test_cart_pickup_locations_today_availability(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that cart pickup locations show Today availability for products in main FFC"""
    print(
        f"{os.linesep}Running test to verify Today availability type...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    # Product2 - Main_1 stock is in Illinois FFC
    product_illinois = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product2-main1-stock"),
        None,
    )

    if product_illinois is None:
        pytest.skip("Test product not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_illinois["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    today_locations = [
        loc for loc in result["items"] if loc.get("availabilityType") == "Today"
    ]

    assert len(today_locations) > 0, "No locations with Today availability found"


    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )


@pytest.mark.graphql
@allure.title("Cart pickup locations - verify Transfer availability type (GraphQL)")
def test_cart_pickup_locations_transfer_availability(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that cart pickup locations show Transfer availability for products requiring transfer"""
    print(
        f"{os.linesep}Running test to verify Transfer availability type...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    # Product5 is only in Billund FFC - requires transfer to other locations
    product_billund = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product5-transfer-b2b"),
        None,
    )

    if product_billund is None:
        pytest.skip("Test product not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_billund["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    # Locations with transfer from Billund should have Transfer or GlobalTransfer availability
    transfer_locations = [
        loc for loc in result["items"]
        if loc.get("availabilityType") in ["Transfer", "GlobalTransfer"]
    ]

    assert len(transfer_locations) > 0, "No locations with Transfer availability found"

    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )


@pytest.mark.graphql
@allure.title("Cart pickup locations - verify all availability types present (GraphQL)")
def test_cart_pickup_locations_all_availability_types(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that cart pickup locations return valid availability types"""
    print(
        f"{os.linesep}Running test to verify all availability types...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

        
    product_multi_region = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product4-main-transfer"),
        None,
    )

    if product_multi_region is None:
        pytest.skip("Test product not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_multi_region["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    # Collect all availability types
    availability_types = set()
    for loc in result["items"]:
        if loc.get("availabilityType"):
            availability_types.add(loc["availabilityType"])

    # Valid availability types
    valid_types = {"Today", "Transfer", "GlobalTransfer"}

    for avail_type in availability_types:
        assert avail_type in valid_types, \
            f"Invalid availability type: {avail_type}"

    print(f"Found availability types: {availability_types}")

    # Count by type
    today_count = len([l for l in result["items"] if l.get("availabilityType") == "Today"])
    transfer_count = len([l for l in result["items"] if l.get("availabilityType") == "Transfer"])
    global_transfer_count = len([l for l in result["items"] if l.get("availabilityType") == "GlobalTransfer"])

    print(f"Today: {today_count}, Transfer: {transfer_count}, GlobalTransfer: {global_transfer_count}")

    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )


@pytest.mark.graphql
@allure.title("Cart pickup locations - Today availability has higher priority (GraphQL)")
def test_cart_pickup_locations_today_priority(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    """Test that Today availability locations appear before Transfer locations"""
    print(
        f"{os.linesep}Running test to verify Today availability priority...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    pickup_locations_operations = PickupLocationsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    # Product with stock in Illinois FFC
    product = next(
        (p for p in dataset["products"] if p["id"] == "product-acme-product2-main1-stock"),
        None,
    )

    if product is None:
        pytest.skip("Test product not found in dataset")

    cart = cart_operations.add_item_to_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product["id"],
            "quantity": 1,
        }
    )

    result = pickup_locations_operations.get_cart_pickup_locations(
        cart_id=cart["id"],
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    # First location should have Today availability if any Today exists
    today_locations = [l for l in result["items"] if l.get("availabilityType") == "Today"]

    if len(today_locations) > 0 and len(result["items"]) > 0:
        first_location = result["items"][0]
        assert first_location.get("availabilityType") == "Today", \
            f"First location should have Today availability, got {first_location.get('availabilityType')}"
        print("Verified: Today availability locations appear first")
    else:
        print("No Today availability locations found or empty result")

    cart_operations.clear_cart(
        {
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartId": cart["id"],
        }
    )
