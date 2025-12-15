import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Search organization contacts by name (GraphQL)")
def test_search_organization_contacts_by_name(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to search organization contacts by name...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="Employee",
    )

    auth.clear_token()

    assert (
        organization_contacts["contacts"]["totalCount"] > 0
    ), "Organization contacts not found"


@pytest.mark.graphql
@allure.title("Search organization contacts by email (GraphQL)")
def test_search_organization_contacts_by_email(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to search organization contacts by email...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="administrator@acme.com",
    )

    auth.clear_token()

    assert (
        organization_contacts["contacts"]["totalCount"] > 0
    ), "Organization contacts not found"
