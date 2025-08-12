import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1


@pytest.mark.graphql
@allure.title("Update organization address (GraphQL)")
def test_update_organization_address(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(
        config["test_permanent_corporate_customer_username"],
        config["test_permanent_corporate_customer_password"],
    )

    user = user_operations.get_user()

    contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [TEST_CUSTOMER_ADDRESS_1],
        }
    )

    added_address = contact["addresses"]["items"][0]

    updated_contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [
                {**added_address, "line1": "1234 Pine Drive"},
            ],
        }
    )

    updated_address = updated_contact["addresses"]["items"][0]

    # Test teardown

    contact_operations.delete_contact_address(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [updated_address],
        }
    )

    auth.clear_token()

    assert updated_address is not None, "Updated address is None"
    assert (
        updated_address["line1"] == "1234 Pine Drive"
    ), "Contact address line1 is not updated"
