import os
from typing import Any, Dict

import allure
import pytest
from gql.transport.exceptions import TransportQueryError

from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Success catalog browsing as anonymous user (GraphQL)")
def test_success_catalog_browsing_as_anonymous_user(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    anonymous_catalog_requests: AnonymousCatalogRequests,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to successfully browse catalog as anonymous user...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(True)

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]

    user = user_operations.get_me()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
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
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["store_id"],
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
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    anonymous_catalog_requests: AnonymousCatalogRequests,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to unsuccessfully browse catalog as anonymous user...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(False)

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    category = dataset["categories"][0]
    product = dataset["products"][0]

    user = user_operations.get_me()

    with pytest.raises(TransportQueryError) as categories_exc_info:
        categories_operations.get_categories(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            filter=f"category.subtree:{catalog['id']}",
        )

    with pytest.raises(TransportQueryError) as category_exc_info:
        categories_operations.get_category(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            id=category["id"],
        )

    with pytest.raises(TransportQueryError) as products_exc_info:
        products_operations.get_products(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=currency,
            culture_name=culture,
            filter=f"category.subtree:{catalog['id']}/{category['id']}",
        )

    with pytest.raises(TransportQueryError) as product_exc_info:
        products_operations.get_product(
            store_id=config["store_id"],
            user_id=user["id"],
            culture_name=culture,
            currency_code=currency,
            id=product["id"],
        )

    # Test teardown

    anonymous_catalog_requests.toggle(True)

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
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to browse catalog as registered user...", end=" ")

    anonymous_catalog_requests.toggle(False)

    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]

    auth.authenticate(
        username=dataset["users"][0]["userName"],
        password=config["users_password"],
    )

    user = user_operations.get_me()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
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
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=product_to_compare["id"],
    )

    auth.clear_token()

    # Test teardown

    anonymous_catalog_requests.toggle(True)

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"
