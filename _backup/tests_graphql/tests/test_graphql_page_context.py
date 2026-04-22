import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.page_context.page_context_operations import PageContextOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get page context with store info (GraphQL)")
def test_get_page_context_store_info(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get page context with store info...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)

    culture = dataset["languages"][0]["allowedValues"][0]

    page_context = page_context_operations.get_store_context(
        store_id=config["STORE_ID"],
        domain=config["FRONTEND_BASE_URL"],
        permalink="/",
        culture_name=culture,
    )

    assert page_context is not None, "Page context is None"
    assert page_context["store"] is not None, "Store info is None"
    assert page_context["store"]["storeId"] == config["STORE_ID"], "Store ID does not match"
    assert page_context["store"]["storeName"] is not None, "Store name is None"
    assert page_context["store"]["defaultCurrency"] is not None, "Default currency is None"
    assert page_context["store"]["defaultCurrency"]["code"] is not None, "Currency code is None"
    assert page_context["store"]["defaultLanguage"] is not None, "Default language is None"
    assert page_context["store"]["defaultLanguage"]["cultureName"] is not None, "Culture name is None"
    assert page_context["store"]["availableLanguages"] is not None, "Available languages is None"
    assert len(page_context["store"]["availableLanguages"]) > 0, "Available languages is empty"


@pytest.mark.graphql
@allure.title("Get page context with slug info (GraphQL)")
def test_get_page_context_slug_info(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get page context with slug info...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    dataset_product = dataset["products"][1]

    user = user_operations.get_me()

    # Get the product to obtain its slug
    product = products_operations.get_product(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=dataset_product["id"],
    )

    page_context = page_context_operations.get_slug_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        permalink=product["slug"],
    )

    assert page_context is not None, "Page context is None"
    assert page_context["slugInfo"] is not None, "Slug info is None"
    assert page_context["slugInfo"]["entityInfo"] is not None, "Entity info is None"
    assert page_context["slugInfo"]["entityInfo"]["semanticUrl"] is not None, "Semantic URL is None"
    assert (
        page_context["slugInfo"]["entityInfo"]["semanticUrl"] == product["seoInfo"]["semanticUrl"]
    ), "Semantic URL does not match product SEO info"
    assert (
        page_context["slugInfo"]["entityInfo"]["objectId"] == dataset_product["id"]
    ), "Object ID does not match product ID"
    assert page_context["slugInfo"]["entityInfo"]["objectType"] == "CatalogProduct", "Object type is not CatalogProduct"
    assert page_context["slugInfo"]["entityInfo"]["isActive"] is True, "Slug is not active"


@pytest.mark.graphql
@allure.title("Get page context with category slug info (GraphQL)")
def test_get_page_context_category_slug_info(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get page context with category slug info...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    dataset_category = dataset["categories"][0]

    user = user_operations.get_me()

    # Get the category to obtain its slug
    category = categories_operations.get_category(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=dataset_category["id"],
    )

    page_context = page_context_operations.get_slug_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        permalink=category["slug"],
    )

    assert page_context is not None, "Page context is None"
    assert page_context["slugInfo"] is not None, "Slug info is None"
    assert page_context["slugInfo"]["entityInfo"] is not None, "Entity info is None"
    assert page_context["slugInfo"]["entityInfo"]["semanticUrl"] is not None, "Semantic URL is None"
    assert (
        page_context["slugInfo"]["entityInfo"]["semanticUrl"] == category["seoInfo"]["semanticUrl"]
    ), "Semantic URL does not match category SEO info"
    assert (
        page_context["slugInfo"]["entityInfo"]["objectId"] == dataset_category["id"]
    ), "Object ID does not match category ID"
    assert page_context["slugInfo"]["entityInfo"]["objectType"] == "Category", "Object type is not Category"
    assert page_context["slugInfo"]["entityInfo"]["isActive"] is True, "Slug is not active"


@pytest.mark.graphql
@allure.title("Get page context with slug info for authenticated user (GraphQL)")
def test_get_page_context_slug_info_authenticated_user(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient, auth: Auth
):
    print(f"{os.linesep}Running test to get page context with slug info for authenticated user...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    dataset_user = dataset["users"][0]
    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    dataset_product = dataset["products"][1]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

    # Get the product to obtain its slug
    product = products_operations.get_product(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=dataset_product["id"],
    )

    try:
        page_context = page_context_operations.get_slug_context(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            culture_name=culture,
            permalink=product["slug"],
        )
    finally:
        auth.clear_token()

    assert page_context is not None, "Page context is None"
    assert page_context["slugInfo"] is not None, "Slug info is None"
    assert page_context["slugInfo"]["entityInfo"] is not None, "Entity info is None"
    assert page_context["slugInfo"]["entityInfo"]["semanticUrl"] is not None, "Semantic URL is None"
    assert (
        page_context["slugInfo"]["entityInfo"]["semanticUrl"] == product["seoInfo"]["semanticUrl"]
    ), "Semantic URL does not match product SEO info"
    assert (
        page_context["slugInfo"]["entityInfo"]["objectId"] == dataset_product["id"]
    ), "Object ID does not match product ID"
    assert page_context["slugInfo"]["entityInfo"]["objectType"] == "CatalogProduct", "Object type is not CatalogProduct"
    assert page_context["slugInfo"]["entityInfo"]["isActive"] is True, "Slug is not active"


@pytest.mark.graphql
@allure.title("Get page context for anonymous user (GraphQL)")
def test_get_page_context_anonymous_user(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient, auth: Auth
):
    print(f"{os.linesep}Running test to get page context for anonymous user...", end=" ")

    auth.clear_token()

    page_context_operations = PageContextOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    user = user_operations.get_me()

    page_context = page_context_operations.get_user_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
    )

    assert page_context is not None, "Page context is None"
    assert page_context["user"] is not None, "User info is None"
    assert page_context["user"]["id"] is not None, "User ID is None"
    assert page_context["user"]["userName"] == "Anonymous", "User name is not Anonymous"


@pytest.mark.graphql
@allure.title("Get page context for authenticated user (GraphQL)")
def test_get_page_context_authenticated_user(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get page context for authenticated user...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    dataset_user = dataset["users"][0]
    dataset_contact = dataset["contacts"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

    page_context = page_context_operations.get_user_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    auth.clear_token()

    assert page_context is not None, "Page context is None"
    assert page_context["user"] is not None, "User info is None"
    assert page_context["user"]["id"] is not None, "User ID is None"
    assert page_context["user"]["id"] == user["id"], "User ID does not match"
    assert page_context["user"]["userName"] == dataset_user["userName"], "User name does not match"
    assert page_context["user"]["contact"]["organizations"] is not None, "Contact organizations is None"
    assert page_context["user"]["contact"]["organizations"]["items"] is not None, "Contact organizations items is None"
    assert (
        len(page_context["user"]["contact"]["organizations"]["items"]) == 10
    ), "Contact organizations count does not match"

    organization_ids = [org["id"] for org in page_context["user"]["contact"]["organizations"]["items"]]
    assert dataset_contact["defaultOrganizationId"] in organization_ids, (
        f"Default organization '{dataset_contact['defaultOrganizationId']}' not found in organizations list. "
        f"Found: {organization_ids}"
    )


@pytest.mark.ignore
@pytest.mark.graphql
@allure.title("Get page context with white labeling settings (GraphQL)")
def test_get_page_context_white_labeling(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient, auth: Auth
):
    print(f"{os.linesep}Running test to get page context with white labeling settings...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    dataset_user = dataset["users"][0]
    dataset_contact = dataset["contacts"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

    page_context = page_context_operations.get_white_labeling_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    auth.clear_token()

    assert page_context is not None, "Page context is None"
    # White labeling settings may be None if not configured for the store
    # The test verifies the query executes successfully and the field is present
    assert "whiteLabelingSettings" in page_context, "White labeling settings field is missing from response"


@pytest.mark.graphql
@allure.title("Get full page context (GraphQL)")
def test_get_full_page_context(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient, auth: Auth):
    print(f"{os.linesep}Running test to get full page context...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)
    user_operations = UserOperations(graphql_client)
    dataset_user = dataset["users"][0]
    dataset_contact = dataset["contacts"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()
    culture = dataset["languages"][0]["allowedValues"][0]

    page_context = page_context_operations.get_page_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        permalink="catalog",
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    auth.clear_token()

    assert page_context is not None, "Page context is None"
    assert page_context["store"] is not None, "Store info is None"
    assert page_context["store"]["storeId"] == config["STORE_ID"], "Store ID does not match"
    assert page_context["user"] is not None, "User info is None"
    assert page_context["user"]["id"] is not None, "User ID is None"
    assert page_context["user"]["contact"] is not None, "User contact is None"
    assert page_context["user"]["contact"]["id"] is not None, "User contact ID is None"
    assert page_context["user"]["contact"]["firstName"] is not None, "User contact first name is None"
    assert page_context["user"]["contact"]["lastName"] is not None, "User contact last name is None"
    assert page_context["user"]["contact"]["organizationId"] is not None, "User contact organization ID is None"
    assert page_context["slugInfo"] is not None, "Slug info is None"
    assert page_context["slugInfo"]["entityInfo"] is not None, "Entity info is None"
    assert page_context["slugInfo"]["entityInfo"]["semanticUrl"] is not None, "Semantic URL is None"
    assert page_context["slugInfo"]["entityInfo"]["semanticUrl"] == "catalog", "Semantic URL does not match catalog"
    assert page_context["slugInfo"]["entityInfo"]["objectId"] is not None, "Object ID is None"
    assert page_context["slugInfo"]["entityInfo"]["objectType"] is not None, "Object type is None"
    assert page_context["slugInfo"]["entityInfo"]["objectType"] == "Catalog", "Object type is not Catalog"
    assert page_context["slugInfo"]["entityInfo"]["isActive"] is True, "Slug is not active"
    # White labeling settings field should be present (may be None if not configured)
    assert "whiteLabelingSettings" in page_context, "White labeling settings field is missing from response"
