import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from utils.generate_invitation_link_mock import generate_invitation_link


@pytest.mark.graphql
@allure.feature("Generate Invitation Link Utility (GraphQL)")
def test_generate_invitation_link_mock(
    config: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
    webapi_client,
):
    """
    Test the generate_invitation_link utility function.
    
    This test verifies that:
    1. The utility successfully invites a user
    2. A valid password reset token is generated
    3. The invitation link is properly formatted
    4. All required query parameters are present
    """
    print(f"{os.linesep}Testing generate_invitation_link utility...", end=" ")

    user_operations = UserOperations(graphql_client)

    # Authenticate using credentials from .env file (user must have an organization)
    auth.authenticate(
        config["username"],
        config["users_password"],
    )

    # Get user info to get their organization ID
    user = user_operations.get_me()
    organization_id = user["contact"]["organizationId"]
    
    print(f"{os.linesep}Using organization ID: {organization_id}")

    # Define test email
    test_email = "test-invitation-utility@example.com"

    # Call the utility function
    invitation_link = generate_invitation_link(
        graphql_client=graphql_client,
        webapi_client=webapi_client,
        config=config,
        email=test_email,
        organization_id=organization_id,
    )

    # Verify the invitation link format
    assert invitation_link is not None, "Invitation link should not be None"
    assert config["frontend_base_url"] in invitation_link, "Link should contain frontend base URL"
    assert "/sign-up?" in invitation_link, "Link should contain sign-up path"
    assert "token=" in invitation_link, "Link should contain token parameter"
    assert "userId=" in invitation_link, "Link should contain userId parameter"
    
    print(f"{os.linesep}Generated invitation link: {invitation_link}")

    # Verify the user was created
    invited_user = user_operations.get_user_by_username(test_email)
    assert invited_user is not None, "Invited user should exist"
    assert invited_user["userName"] == test_email, "Username should match"
    
    # Extract userId from the link and verify it matches
    user_id_from_link = invitation_link.split("userId=")[1].split("&")[0] if "&" in invitation_link.split("userId=")[1] else invitation_link.split("userId=")[1]
    assert user_id_from_link == invited_user["id"], "User ID in link should match invited user ID"

    # Test teardown: Clean up the invited user
    contact_operations = ContactOperations(graphql_client)
    
    # Get the contact
    invited_contacts = contact_operations.fetch_organization_contacts(
        organization_id=organization_id,
        user_id=user["id"],
        search_phrase=test_email,
    )
    
    if invited_contacts and invited_contacts.get("contacts", {}).get("items"):
        invited_contact = invited_contacts["contacts"]["items"][0]
        
        # Remove contact from organization
        contact_operations.remove_contact_from_organization(
            payload={
                "contactId": invited_contact["id"],
                "organizationId": organization_id,
            }
        )
        
        # Delete contact
        contact_operations.delete_contact(
            payload={
                "contactId": invited_contact["id"],
            }
        )
    
    # Delete user
    user_operations.delete_users(
        payload={
            "userNames": [test_email],
        }
    )

    auth.clear_token()

    print(f"{os.linesep}✓ Invitation link utility test passed!")

