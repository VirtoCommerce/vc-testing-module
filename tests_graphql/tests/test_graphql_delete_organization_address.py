import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Delete organization address (GraphQL)")
def test_delete_organization_address(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to delete organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization = contact_operations.fetch_organization_addresses(
        user["contact"]["organizationId"], user["id"]
    )

    organization_original_address = organization["addresses"]["items"][0]
    del organization_original_address["isFavorite"]

    address_to_add = {
        **organization_original_address,
        "id": "temp-address-id",
        "line1": "1234 Some Street",
        "line2": "Some Flat",
    }

    added_address = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [address_to_add],
        }
    )["addresses"]["items"][0]

    contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [organization_original_address],
        }
    )

    # Test teardown

    updated_contact = contact_operations.delete_contact_address(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [added_address],
        }
    )

    auth.clear_token()

    assert (
        len(updated_contact["addresses"]["items"]) == 1
    ), "Contact addresses are not deleted"
