import os
from typing import Any, Dict

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Delete organization address (GraphQL)")
def test_delete_organization_address(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to delete organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["users_password"],
    )

    user = user_operations.get_me()

    organization = contact_operations.fetch_organization_addresses(
        user["contact"]["organizationId"], user["id"]
    )

    organization_original_address = organization["addresses"]["items"][0]

    address_to_add = {
        **organization_original_address,
        "id": "temp-address-id",
        "line1": "1234 Some Street",
        "line2": "Some Flat",
    }
    del address_to_add["isFavorite"]

    added_address = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [address_to_add],
        }
    )["addresses"]["items"][0]

    updated_contact = contact_operations.delete_contact_address(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [added_address],
        }
    )

    organization = contact_operations.fetch_organization_addresses(
        user["contact"]["organizationId"], user["id"]
    )

    auth.clear_token()

    assert (
        len(updated_contact["addresses"]["items"]) == 1
    ), "Contact addresses are not deleted"
