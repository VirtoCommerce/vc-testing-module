import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add address to favorites (GraphQL)")
def test_add_address_to_favorites(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to add address to favorites...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["users_password"],
    )

    user = user_operations.get_me()

    organization = contact_operations.fetch_organization_addresses(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
    )

    contact_operations.add_address_to_favorites(
        payload={"addressId": organization["addresses"]["items"][0]["id"]}
    )

    contact_operations.remove_address_from_favorites(
        payload={"addressId": organization["addresses"]["items"][0]["id"]}
    )

    organization = contact_operations.fetch_organization_addresses(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
    )

    # Test teardown

    auth.clear_token()

    assert (
        len(organization["addresses"]["items"]) == 1
    ), "Organization addresses quantity mismatch"
    assert (
        organization["addresses"]["items"][0]["isFavorite"] is False
    ), "Favorite address is not removed"
