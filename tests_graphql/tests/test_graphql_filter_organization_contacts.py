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
@allure.title("Filter organization contacts by role (GraphQL)")
def test_filter_organization_contacts_by_role(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to filter organization contacts by role...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization_maintainers = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'org-maintainer'",
    )

    organization_employees = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'org-employee'",
    )

    purchasing_agents = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'purchasing-agent'",
    )

    store_administrators = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'store-admin'",
    )

    store_managers = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'store-manager'",
    )

    auth.clear_token()

    assert (
        organization_maintainers["contacts"]["totalCount"] > 0
    ), "Organization maintainers not found"
    assert (
        organization_employees["contacts"]["totalCount"] > 0
    ), "Organization employees not found"
    assert (
        purchasing_agents["contacts"]["totalCount"] > 0
    ), "Purchasing agents not found"
    assert (
        store_administrators["contacts"]["totalCount"] > 0
    ), "Store administrators not found"
    assert store_managers["contacts"]["totalCount"] > 0, "Store managers not found"


@pytest.mark.graphql
@allure.title("Filter organization contacts by status (GraphQL)")
def test_filter_organization_contacts_by_status(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to filter organization contacts by status...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    active_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'status':'Approved'",
    )

    invited_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'status':'Invited'",
    )

    blocked_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'status':'Locked'",
    )

    auth.clear_token()

    assert active_contacts["contacts"]["totalCount"] > 0, "Active contacts not found"
    assert invited_contacts["contacts"]["totalCount"] > 0, "Invited contacts not found"
    assert blocked_contacts["contacts"]["totalCount"] > 0, "Blocked contacts not found"
