import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Change organization contact role (GraphQL)")
def test_change_organization_contact_role(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to change organization contact role...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(
        config["test_permanent_corporate_customer_username"],
        config["test_permanent_corporate_customer_password"],
    )

    user = user_operations.get_user()

    organization_contact_to_change_role = (
        contact_operations.fetch_organization_contacts(
            organization_id=user["contact"]["organizationId"],
            user_id=user["id"],
            search_phrase="e2e-test-purchasing-agent@e2e-contoso.com",
        )["contacts"]["items"][0]
    )

    result = contact_operations.change_organization_contact_role(
        payload={
            "roleIds": ["org-employee"],
            "userId": organization_contact_to_change_role["securityAccounts"][0]["id"],
        }
    )

    changed_contact = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-purchasing-agent@e2e-contoso.com",
    )["contacts"]["items"][0]

    # Test teardown
    contact_operations.change_organization_contact_role(
        payload={
            "roleIds": ["purchasing-agent"],
            "userId": organization_contact_to_change_role["securityAccounts"][0]["id"],
        }
    )

    auth.clear_token()

    assert result["succeeded"] == True, "Contact role was not changed"
    assert (
        changed_contact["securityAccounts"][0]["roles"][0]["id"] == "org-employee"
    ), "Contact role was not changed"
