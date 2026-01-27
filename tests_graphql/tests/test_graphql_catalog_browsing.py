import os
from typing import Any

import allure
import pytest
from gql.transport.exceptions import TransportQueryError

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Success catalog browsing as anonymous user (GraphQL)")
def test_success_catalog_browsing_as_anonymous_user(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to successfully browse catalog as anonymous user...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    catalog = dataset["catalogs"][0]

    user = user_operations.get_me()

    categories_response = categories_operations.get_categories(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}",
    )

    category_to_compare = next(
        category
        for category in categories_response["items"]
        if category["id"] == "category-acme-laptops"
    )

    category = categories_operations.get_category(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=product_to_compare["id"],
    )

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"


@pytest.mark.graphql
@allure.title("Unsuccess catalog browsing as anonymous user (GraphQL)")
def test_unsuccess_catalog_browsing_as_anonymous_user(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
    webapi_client: WebAPISession,
):
    print(
        f"{os.linesep}Running test to unsuccessfully browse catalog as anonymous user...",
        end=" ",
    )

    auth.authenticate(
        username=config["ADMIN_USERNAME"],
        password=config["USERS_PASSWORD"],
    )
    webapi_client.patch(
        f"/api/stores/{config['STORE_ID']}",
        data=[{"op": "replace", "path": "/settings/1/value", "value": False}],
    )
    auth.clear_token()

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    catalog = dataset["catalogs"][0]
    category = dataset["categories"][0]
    product = dataset["products"][0]

    user = user_operations.get_me()

    with pytest.raises(TransportQueryError) as categories_exc_info:
        categories_operations.get_categories(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            filter=f"category.subtree:{catalog['id']}",
        )

    with pytest.raises(TransportQueryError) as category_exc_info:
        categories_operations.get_category(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            id=category["id"],
        )

    with pytest.raises(TransportQueryError) as products_exc_info:
        products_operations.get_products(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            filter=f"category.subtree:{catalog['id']}/{category['id']}",
        )

    with pytest.raises(TransportQueryError) as product_exc_info:
        products_operations.get_product(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            culture_name=culture,
            currency_code=currency,
            id=product["id"],
        )

    auth.authenticate(
        username=config["ADMIN_USERNAME"],
        password=config["USERS_PASSWORD"],
    )
    webapi_client.patch(
        f"/api/stores/{config['STORE_ID']}",
        data=[{"op": "replace", "path": "/settings/1/value", "value": True}],
    )
    auth.clear_token()

    # Test teardown

    assert (
        categories_exc_info.value.errors[0]["extensions"]["code"] == "Unauthorized"
    ), "Categories query should return Unauthorized error"
    assert (
        category_exc_info.value.errors[0]["extensions"]["code"] == "Unauthorized"
    ), "Category query should return Unauthorized error"
    assert (
        products_exc_info.value.errors[0]["extensions"]["code"] == "Unauthorized"
    ), "Products query should return Unauthorized error"
    assert (
        product_exc_info.value.errors[0]["extensions"]["code"] == "Unauthorized"
    ), "Product query should return Unauthorized error"


@pytest.mark.graphql
@allure.title("Catalog browsing as registered user (GraphQL)")
def test_catalog_browsing_as_registered_user(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to browse catalog as registered user...", end=" ")

    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    catalog = dataset["catalogs"][0]

    auth.authenticate(
        username=dataset["users"][0]["userName"],
        password=config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    categories_response = categories_operations.get_categories(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}",
    )

    category_to_compare = next(
        category
        for category in categories_response["items"]
        if category["id"] == "category-acme-laptops"
    )

    category = categories_operations.get_category(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=product_to_compare["id"],
    )

    auth.clear_token()

    # Test teardown

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"
