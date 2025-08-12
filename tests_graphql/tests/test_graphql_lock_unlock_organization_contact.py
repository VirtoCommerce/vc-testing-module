import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Lock and unlock organization contact (GraphQL)")
def test_lock_unlock_organization_contact(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to lock and unlock organization contact...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(
        config["test_permanent_corporate_customer_username"],
        config["test_permanent_corporate_customer_password"],
    )

    user = user_operations.get_user()

    organization_contact_to_lock = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-employee-1@e2e-contoso.com",
    )["contacts"]["items"][0]

    locked_contact = contact_operations.lock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    unlocked_contact = contact_operations.unlock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    auth.clear_token()

    assert locked_contact["status"] == "Locked", "Contact is not locked"
    assert unlocked_contact["status"] == "Approved", "Contact is not unlocked"
