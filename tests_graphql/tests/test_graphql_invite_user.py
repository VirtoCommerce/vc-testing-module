import os
import random
import time
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Invite user (GraphQL)")
def test_invite_user(
    config: Config, auth: Auth, dataset: dict[str, Any], graphql_client: GraphQLClient, webapi_client: WebAPISession
):
    print(f"{os.linesep}Running test to invite user...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(user for user in dataset["users"] if user["id"] == "user-acme-store-maintainer-1")

    dataset_organization = next(
        organization
        for organization in dataset["organizations"]
        if organization["id"] == dataset["contacts"][9]["defaultOrganizationId"]
    )

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    maintainer_user = user_operations.get_me()
    invite_employee_email = f"invite-employee-{random.randint(1000, 9999)}@acme.com"

    invitation_result = contact_operations.invite_user(
        payload={
            "storeId": config["STORE_ID"],
            "organizationId": dataset_organization["id"],
            "emails": [invite_employee_email],
            "message": "You are invited to join the organization",
            "roleIds": ["org-employee"],
            "urlSuffix": "/confirm-invitation",
        }
    )

    if invitation_result["succeeded"] == False:
        raise Exception(f"{os.linesep}Invitation failed: {invitation_result['errors'][0]}")

    auth.authenticate(
        config["ADMIN_USERNAME"],
        config["ADMIN_PASSWORD"],
    )

    time.sleep(20)

    invited_contact = contact_operations.fetch_organization_contacts(
        organization_id=dataset_organization["id"],
        user_id=maintainer_user["id"],
        search_phrase=invite_employee_email,
    )["contacts"]["items"][0]

    # Test teardown

    contact_operations.remove_contact_from_organization(
        payload={
            "contactId": invited_contact["id"],
            "organizationId": dataset_organization["id"],
        }
    )

    contact_operations.delete_contact(
        payload={
            "contactId": invited_contact["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": [invite_employee_email],
        }
    )

    auth.clear_token()

    assert invitation_result["succeeded"] == True, "User was not invited"
    assert invited_contact is not None, "Invited contact was not found"
    assert invited_contact["status"] == "Invited", "Invited contact status is not Invited"
    assert invited_contact["emails"][0] == invite_employee_email, "Invited contact email is not the same"
