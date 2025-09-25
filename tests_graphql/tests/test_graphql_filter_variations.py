import os
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_catalog import MIXED_CATALOG
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_2


@pytest.mark.ignore
@pytest.mark.graphql
@allure.feature("Filter product variations by stock (GraphQL)")
def test_filter_product_variations_by_stock(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to filter product variations by stock...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    search_variations_result_all = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation",
    )

    search_variations_result_in_stock = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation availability:InStock",
    )

    assert (
        search_variations_result_all["totalCount"] == 3
    ), "Total count of variations is not correct"
    assert (
        search_variations_result_in_stock["totalCount"] == 2
    ), "Total count of variations in stock is not correct"


@pytest.mark.ignore
@pytest.mark.graphql
@allure.feature("Filter product variations by price (GraphQL)")
def test_filter_product_variations_by_price(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to filter product variations by price...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    search_variations_result_800_900 = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"price\":[800 TO 900)",
    )

    search_variations_result_900_1000 = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"price\":[900 TO 1000)",
    )

    search_variations_result_1000_1500 = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"price\":[1000 TO 1500)",
    )

    assert (
        search_variations_result_800_900["totalCount"] == 1
    ), "Total count of variations with price between 800 and 900 is not correct"
    assert (
        search_variations_result_900_1000["totalCount"] == 1
    ), "Total count of variations with price between 900 and 1000 is not correct"
    assert (
        search_variations_result_1000_1500["totalCount"] == 1
    ), "Total count of variations with price between 1000 and 1500 is not correct"


@pytest.mark.ignore
@pytest.mark.graphql
@allure.feature("Filter product variations by property (GraphQL)")
def test_filter_product_variations_by_property(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to filter product variations by property...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    search_variations_result_8gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"RAM\":\"8Gb\"",
    )

    search_variations_result_16gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"RAM\":\"16Gb\"",
    )

    search_variations_result_32gb = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation \"RAM\":\"32Gb\"",
    )

    assert (
        search_variations_result_8gb["totalCount"] == 2
    ), "Total count of variations with 8Gb RAM is not correct"
    assert (
        search_variations_result_16gb["totalCount"] == 0
    ), "Total count of variations with 16Gb RAM is not correct"
    assert (
        search_variations_result_32gb["totalCount"] == 2
    ), "Total count of variations with 32Gb RAM is not correct"
