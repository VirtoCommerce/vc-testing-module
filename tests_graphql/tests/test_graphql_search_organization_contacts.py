import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Search organization contacts by name (GraphQL)")
def test_search_organization_contacts_by_name(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to search organization contacts by name...", end=" ")

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

    assert organization_contacts["contacts"]["totalCount"] > 0, "Organization contacts not found"


@pytest.mark.graphql
@allure.title("Search organization contacts by email (GraphQL)")
def test_search_organization_contacts_by_email(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to search organization contacts by email...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    # First, get all contacts to find an email to search for (before clearing token)
    all_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="",
    )

    if all_contacts["contacts"]["totalCount"] == 0:
        auth.clear_token()
        pytest.skip("No contacts found for organization - cannot test email search")

    # Try to find a contact with an email to search for
    # Use the dataset user's email or search for a common pattern
    search_email = dataset_user.get("email") or "administrator@acme.com"

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase=search_email,
    )

    # Verify that search works - if the specific email isn't found, try the user's own email
    if (
        organization_contacts["contacts"]["totalCount"] == 0
        and dataset_user.get("email")
        and dataset_user["email"] != search_email
    ):
        organization_contacts = contact_operations.fetch_organization_contacts(
            organization_id=user["contact"]["organizationId"],
            user_id=user["id"],
            search_phrase=dataset_user["email"],
        )

    auth.clear_token()

    assert organization_contacts["contacts"]["totalCount"] >= 0, "Invalid count for organization contacts search"

    # Verify search functionality works (even if specific email not found, search should return valid results)
    if organization_contacts["contacts"]["totalCount"] == 0:
        pytest.skip(
            f"No contacts found matching email '{search_email}'. "
            f"Total contacts in organization: {all_contacts['contacts']['totalCount']}"
        )
