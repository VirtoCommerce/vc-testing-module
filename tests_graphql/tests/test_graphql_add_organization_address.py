import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.title("Add organization address (GraphQL)")
def test_add_organization_address(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(
        TEST_PERMANENT_CORPORATE_USER["username"],
        TEST_PERMANENT_CORPORATE_USER["password"],
    )

    user = user_operations.get_user()

    contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [TEST_CUSTOMER_ADDRESS_1],
        }
    )

    added_address = contact["addresses"]["items"][0]

    # Test teardown

    contact_operations.delete_contact_address(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [added_address],
        }
    )

    auth.clear_token()

    assert contact["addresses"]["items"] is not None, "Contact addresses are None"
    assert len(contact["addresses"]["items"]) > 0, "Contact addresses are empty"
