import os
from typing import Any, Dict

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Registration by invitation (GraphQL)")
def test_graphql_registration_by_invitation(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient, webapi_client, dataset: dict[str, Any]
):
    print(
        f"{os.linesep}Running GraphQL test to register a user by invitation...", end=" "
    )

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-maintainer-1"
    )

    dataset_organization = next(
        organization
        for organization in dataset["organizations"]
        if organization["id"] == dataset["contacts"][9]["defaultOrganizationId"]
    )

    auth.authenticate(
        dataset_user["userName"],
        config["users_password"],
    )    

    contact_operations.invite_user(
        payload={
            "storeId": config["store_id"],
            "organizationId": dataset_organization["id"],
            "emails": ["e2e-test-corporate-temp@test.com"],
            "message": "You are invited to join the organization",
            "roleIds": ["org-employee"],
            "urlSuffix": "/confirm-invitation"  
        }
    )

    invited_user = user_operations.get_user_by_username(
        "e2e-test-corporate-temp@test.com"
    )

    auth.authenticate(
        config["admin_username"],
        config["admin_password"],
    )

    token = webapi_client.get(
        f"/api/platform/security/users/{invited_user['id']}/generatePasswordResetToken"
    )        

    register_result = user_operations.register_by_invitation(
        payload={
            "userId": invited_user["id"],
            "username": invited_user["userName"],
            "password": "Password1!",
            "token": token,
            "firstName": "[E2E Test]",
            "lastName": "Temp E2E Test User",
        }
    )

    # Test teardown

    contact_operations.delete_contact(
        payload={
            "contactId": invited_user["contact"]["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": ["e2e-test-corporate-temp@test.com"],
        }
    )

    auth.clear_token()

    assert register_result["succeeded"] is True
