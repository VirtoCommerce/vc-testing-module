import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.page_context.page_context_operations import PageContextOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get page context with store info (GraphQL)")
def test_get_page_context_store_info(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get page context with store info...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)

    culture = dataset["languages"][0]["allowedValues"][0]

    page_context = page_context_operations.get_store_context(
        store_id=config["STORE_ID"],
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


@pytest.mark.graphql
@allure.title("Get page context for anonymous user (GraphQL)")
def test_get_page_context_anonymous_user(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get page context for anonymous user...", end=" ")

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
    assert page_context["user"]["userName"] == dataset_user["userName"], "User name does not match"
    assert page_context["user"]["contact"]["organizations"] is not None, "Contact organizations is None"
    assert page_context["user"]["contact"]["organizations"]["items"] is not None, "Contact organizations items is None"
    assert len(page_context["user"]["contact"]["organizations"]["items"]) == 10, "Contact organizations count does not match"
    assert page_context["user"]["contact"]["organizations"]["items"][0]["id"] == dataset_contact["defaultOrganizationId"], "Contact organization ID does not match"


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

    page_context = page_context_operations.get_user_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    auth.clear_token()
 

    page_context = page_context_operations.get_white_labeling_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    assert page_context is not None, "Page context is None"
    # White labeling settings may be None if not configured for the store
    # The test verifies the query executes successfully and the field is present
    assert "whiteLabelingSettings" in page_context, "White labeling settings field is missing from response"


@pytest.mark.graphql
@allure.title("Get full page context (GraphQL)")
def test_get_full_page_context(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient, auth: Auth
):
    print(f"{os.linesep}Running test to get full page context...", end=" ")

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

    culture = dataset["languages"][0]["allowedValues"][0]
    user = user_operations.get_me()

    page_context = page_context_operations.get_page_context(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        organization_id=dataset_contact["defaultOrganizationId"],
    )

    assert page_context is not None, "Page context is None"
    assert page_context["store"] is not None, "Store info is None"
    assert page_context["store"]["storeId"] == config["STORE_ID"], "Store ID does not match"
    assert page_context["user"] is not None, "User info is None"
    assert page_context["user"]["id"] is not None, "User ID is None"
    # White labeling settings field should be present (may be None if not configured)
    assert "whiteLabelingSettings" in page_context, "White labeling settings field is missing from response"


@pytest.mark.graphql
@allure.title("Get page context with available languages (GraphQL)")
def test_get_page_context_available_languages(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get page context with available languages...", end=" ")

    page_context_operations = PageContextOperations(graphql_client)

    culture = dataset["languages"][0]["allowedValues"][0]

    page_context = page_context_operations.get_store_context(
        store_id=config["STORE_ID"],
        culture_name=culture,
    )

    assert page_context is not None, "Page context is None"
    assert page_context["store"] is not None, "Store info is None"
    assert page_context["store"]["availableLanguages"] is not None, "Available languages is None"
    assert len(page_context["store"]["availableLanguages"]) > 0, "Available languages is empty"
    # Verify that each language has required fields
    for language in page_context["store"]["availableLanguages"]:
        assert language["cultureName"] is not None, "Language culture name is None"
        assert language["nativeName"] is not None, "Language native name is None"

