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
from graphql_operations.page_context.page_context_operations import PageContextOperations


DEFAULT_ROLE_ID = "org-employee"
INDEXING_WAIT_SECONDS = 10


@pytest.mark.ignore
@pytest.mark.graphql
@allure.feature("Invite user (GraphQL)")
def test_invite_user(
    config: Config, auth: Auth, dataset: dict[str, Any], graphql_client: GraphQLClient, webapi_client: WebAPISession
):
    print(f"{os.linesep}Running test to invite user...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        (user for user in dataset["users"] if user["id"] == "user-acme-store-maintainer-1"),
        None,
    )
    assert dataset_user is not None, "Could not find dataset user with id 'user-acme-store-maintainer-1'"

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    page_context_operations = PageContextOperations(graphql_client)

    page_context = page_context_operations.get_user_context(
        store_id=config["STORE_ID"],
        user_id=dataset_user["id"],
    )

    organization_id = page_context["user"]["contact"]["organizationId"]
    assert organization_id is not None, "Organization ID is None"

    user_organization = next((org for org in dataset["organizations"] if org["id"] == organization_id), None)
    assert user_organization is not None, f"Could not find organization with ID {organization_id}"

    invite_employee_email = f"invite-employee-{random.randint(1000, 9999)}@acme.com"
    invited_contact = None

    try:
        invitation_result = contact_operations.invite_user(
            payload={
                "storeId": config["STORE_ID"],
                "organizationId": organization_id,
                "emails": [invite_employee_email],
                "message": "You are invited to join the organization",
                "roleIds": [DEFAULT_ROLE_ID],
                "urlSuffix": "/confirm-invitation",
            }
        )

        assert invitation_result["succeeded"] is True, "Invitation operation did not succeed"

        time.sleep(INDEXING_WAIT_SECONDS)

        result = contact_operations.fetch_organization_contacts(
            organization_id=organization_id,
            user_id=dataset_user["id"],
            search_phrase=invite_employee_email,
        )
        contacts = result.get("contacts", {}).get("items", [])

        if not contacts:
            time.sleep(INDEXING_WAIT_SECONDS)
            result = contact_operations.fetch_organization_contacts(
                organization_id=organization_id,
                user_id=dataset_user["id"],
                search_phrase=invite_employee_email,
            )
            contacts = result.get("contacts", {}).get("items", [])

        if contacts:
            invited_contact = contacts[0]
        else:
            raise AssertionError(f"Invited contact with email '{invite_employee_email}' was not found after retry")

        assert invited_contact is not None, "Invited contact was not found"
        assert invited_contact["status"] == "Invited", "Invited contact status is not Invited"
        assert invited_contact["emails"][0] == invite_employee_email, "Invited contact email is not the same"

    finally:

        if invited_contact is not None:
            try:
                auth.authenticate(
                    config["ADMIN_USERNAME"],
                    config["ADMIN_PASSWORD"],
                )

                contact_operations.remove_contact_from_organization(
                    payload={
                        "contactId": invited_contact["id"],
                        "organizationId": organization_id,
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
            except Exception as cleanup_error:
                print(f"{os.linesep}Warning: Cleanup failed: {cleanup_error}")
            finally:
                auth.clear_token()
