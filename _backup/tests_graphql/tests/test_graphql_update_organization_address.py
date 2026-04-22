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
@allure.title("Update organization address (GraphQL)")
def test_update_organization_address(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to update organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization = contact_operations.fetch_organization_addresses(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
    )

    original_address = organization["addresses"]["items"][0]
    del original_address["isFavorite"]

    updated_contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [
                {
                    **original_address,
                    "line1": "1234 Some Street",
                }
            ],
        }
    )

    # Test teardown

    contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [original_address],
        }
    )

    auth.clear_token()

    assert updated_contact["addresses"]["items"][0] is not None, "Updated address is None"
    assert (
        updated_contact["addresses"]["items"][0]["line1"] == "1234 Some Street"
    ), "Contact address line1 is not updated"
