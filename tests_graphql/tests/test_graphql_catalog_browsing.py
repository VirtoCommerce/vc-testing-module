import os
from typing import Any, Dict

import allure
import pytest
from gql.transport.exceptions import TransportQueryError

from fixtures import AnonymousCatalogRequests, Auth, GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_catalog import TEST_CATALOG
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1


@pytest.mark.graphql
@allure.title("Success catalog browsing as anonymous user (GraphQL)")
def test_success_catalog_browsing_as_anonymous_user(
    config: Dict[str, Any],
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

    user = user_operations.get_user()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}",
    )

    category_to_compare = categories_response["items"][0]

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
        id=product_to_compare["id"],
    )

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"


@pytest.mark.graphql
@allure.title("Unsuccess catalog browsing as anonymous user (GraphQL)")
def test_unsuccess_catalog_browsing_as_anonymous_user(
    config: Dict[str, Any],
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

    user = user_operations.get_user()

    with pytest.raises(TransportQueryError) as categories_exc_info:
        categories_operations.get_categories(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=TEST_CURRENCY["USD"],
            culture_name=TEST_CULTURE["en-US"],
            filter=f"category.subtree:{TEST_CATALOG['id']}",
        )

    with pytest.raises(TransportQueryError) as category_exc_info:
        categories_operations.get_category(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=TEST_CURRENCY["USD"],
            culture_name=TEST_CULTURE["en-US"],
            id=TEST_CATEGORY_1["id"],
        )

    with pytest.raises(TransportQueryError) as products_exc_info:
        products_operations.get_products(
            store_id=config["store_id"],
            user_id=user["id"],
            currency_code=TEST_CURRENCY["USD"],
            culture_name=TEST_CULTURE["en-US"],
            filter=f"category.subtree:{TEST_CATALOG['id']}/{TEST_CATEGORY_1['id']}",
        )

    with pytest.raises(TransportQueryError) as product_exc_info:
        products_operations.get_product(
            store_id=config["store_id"],
            user_id=user["id"],
            culture_name=TEST_CULTURE["en-US"],
            currency_code=TEST_CURRENCY["USD"],
            id=TEST_PRODUCT_1["id"],
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
    auth: Auth,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to browse catalog as registered user...", end=" ")

    anonymous_catalog_requests.toggle(False)

    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    auth.authenticate(
        username=config["test_permanent_customer_username"],
        password=config["test_permanent_customer_password"],
    )

    user = user_operations.get_user()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}",
    )

    category_to_compare = categories_response["items"][0]

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
        id=product_to_compare["id"],
    )

    auth.clear_token()

    # Test teardown

    anonymous_catalog_requests.toggle(True)

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"
