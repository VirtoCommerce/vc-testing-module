import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Filter product variations by stock (GraphQL)")
def test_filter_product_variations_by_stock(
    config: dict[str, Any],
    dataset: dict[str, Any],
    graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to filter product variations by stock...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_family_id = dataset["productVariations"][0]["mainProductId"]

    user = user_operations.get_me()

    search_variations_result_all = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation",
    )

    search_variations_result_in_stock = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation inStock:true",
    )

    assert (
        search_variations_result_all["totalCount"] == 4
    ), "Total count of variations is not correct"
    assert (
        search_variations_result_in_stock["totalCount"] == 3
    ), "Total count of variations in stock is not correct"


@pytest.mark.graphql
@allure.feature("Filter product variations by price (GraphQL)")
def test_filter_product_variations_by_price(
    config: dict[str, Any],
    dataset: dict[str, Any],
    graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to filter product variations by price...", end=" ")

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_family_id = dataset["productVariations"][0]["mainProductId"]

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    user = user_operations.get_me()

    search_variations_result_to_1000 = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"price\":[TO 1000]",
    )

    search_variations_result_from_1000_to_1200 = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"price\":[1000 TO 1200]",
    )

    search_variations_result_1400_to = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"price\":[1400 TO]",
    )

    assert (
        search_variations_result_to_1000["totalCount"] == 1
    ), "Total count of variations with price between 0 and 1000 is not correct"
    assert (
        search_variations_result_from_1000_to_1200["totalCount"] == 1
    ), "Total count of variations with price between 1000 and 1200 is not correct"
    assert (
        search_variations_result_1400_to["totalCount"] == 2
    ), "Total count of variations with price between 1400 and is not correct"



@pytest.mark.graphql
@allure.feature("Filter product variations by property (GraphQL)")
def test_filter_product_variations_by_property(
    config: dict[str, Any],
    dataset: dict[str, Any],
    product_variations: list[dict[str, Any]],
    graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to filter product variations by property...", end=" "
    )

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_family_id = product_variations[1]["mainProductId"]

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    user = user_operations.get_me()

    search_variations_result_8gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"RamSize\":\"8\"",
    )

    search_variations_result_16gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"RamSize\":\"16\"",
    )

    search_variations_result_32gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation \"RamSize\":\"32\"",
    )

    assert (
        search_variations_result_8gb["totalCount"] == 1
    ), "Total count of variations with 8Gb RAM is not correct"
    assert (
        search_variations_result_16gb["totalCount"] == 1
    ), "Total count of variations with 16Gb RAM is not correct"
    assert (
        search_variations_result_32gb["totalCount"] == 1
    ), "Total count of variations with 32Gb RAM is not correct"
