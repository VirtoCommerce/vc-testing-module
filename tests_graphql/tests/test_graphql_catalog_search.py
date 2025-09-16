import os
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Catalog search by product full name (GraphQL)")
def test_catalog_search_by_product_full_name(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to search catalog by product full name...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_to_search = dataset["products"][0]

    user = user_operations.get_me()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"],
    )

    searched_product = products_response["items"][0]

    assert (
        products_response["totalCount"] == 1
    ), "Total count of products does not match"
    assert (
        product_to_search["name"] == searched_product["name"]
    ), "Product name does not match"


@pytest.mark.graphql
@allure.title("Catalog search by product name fragment (GraphQL)")
def test_catalog_search_by_product_name_fragment(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to search catalog by product name fragment...",
        end=" ",
    )

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_to_search = dataset["products"][0]

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_me()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"][:4],
    )

    assert products_response["totalCount"] > 1, "Total count of products does not match"


@pytest.mark.graphql
@allure.title("Catalog search by product SKU (GraphQL)")
def test_catalog_search_by_product_sku(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to search catalog by product SKU...", end=" ")

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_to_search = dataset["products"][0]

    user = user_operations.get_me()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["code"],
    )

    searched_product = products_response["items"][0]

    assert (
        products_response["totalCount"] == 1
    ), "Total count of products does not match"
    assert (
        searched_product["code"] == product_to_search["code"]
    ), "Product SKU does not match"


@pytest.mark.graphql
@allure.title("Catalog search by product availability (GraphQL)")
def test_catalog_search_by_product_availability(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to search catalog by product availability...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_to_search = next(
        product
        for product in dataset["products"]
        if product["id"] == "product-acme-laptop-acer-aspire-16-ai"
    )
    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    user = user_operations.get_me()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_browse["id"],
    )

    products_in_stock_only_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"][:4],
        filter=f"category.subtree:{catalog['id']}/{category['id']} availability:InStock",
    )

    products_all_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"][:4],
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    assert (
        products_in_stock_only_response["totalCount"]
        < products_all_response["totalCount"]
    ), "Total count of products in stock only does not match"


@pytest.mark.graphql
@allure.title("Catalog search by product brand (GraphQL)")
def test_catalog_search_by_product_brand(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to search catalog by product brand...", end=" ")

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_to_search = dataset["products"][0]
    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    user = user_operations.get_me()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_browse["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"][:4],
        filter=f"category.subtree:{catalog['id']}/{category['id']} \"BRAND\":\"{product_to_search['vendor']}\"",
    )

    assert (
        products_response["totalCount"] == 4
    ), "Total count of products does not match"


@pytest.mark.graphql
@allure.title("Catalog search by product price (GraphQL)")
def test_catalog_search_by_product_price(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to search catalog by product price...", end=" ")

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    product_to_search = dataset["products"][0]
    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    user = user_operations.get_me()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_browse["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        query=product_to_search["name"][:4],
        filter=f"category.subtree:{catalog['id']}/{category['id']} \"price\":[1000 TO 1500]",
    )

    assert (
        products_response["totalCount"] == 1
    ), "Total count of products does not match"
