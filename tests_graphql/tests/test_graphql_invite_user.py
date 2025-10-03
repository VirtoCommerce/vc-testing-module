import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.ignore
@pytest.mark.graphql
@allure.feature("Invite user (GraphQL)")
def test_invite_user(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to invite user...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-administrator"
    )

    auth.authenticate(
        dataset_user["userName"],
        config["users_password"],
    )

    user = user_operations.get_me()

    invitation_result = contact_operations.invite_user(
        payload={
            "storeId": config["store_id"],
            "organizationId": user["contact"]["organizationId"],
            "emails": ["invite-employee@acme.com"],
            "message": "You are invited to join the organization",
            "roleIds": ["org-employee"],
        }
    )

    if invitation_result["succeeded"] == False:
        raise Exception(
            f"{os.linesep}Invitation failed: {invitation_result['errors'][0]}"
        )

    invited_contact = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="invite-employee@acme.com",
    )["contacts"]["items"][0]

    # Test teardown

    contact_operations.remove_contact_from_organization(
        payload={
            "contactId": invited_contact["id"],
            "organizationId": user["contact"]["organizationId"],
        }
    )

    contact_operations.delete_contact(
        payload={
            "contactId": invited_contact["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": ["invite-employee@acme.com"],
        }
    )

    auth.clear_token()

    assert invitation_result["succeeded"] == True, "User was not invited"
    assert invited_contact is not None, "Invited contact was not found"
    assert (
        invited_contact["status"] == "Invited"
    ), "Invited contact status is not Invited"
