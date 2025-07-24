import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.feature("Invite user (GraphQL)")
def test_invite_user(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to invite user...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    invitation_result = contact_operations.invite_user(
        payload={
            "storeId": config["store_id"],
            "organizationId": user["contact"]["organizationId"],
            "emails": ["e2e-test-corporate-temp@test.com"],
            "message": "You are invited to join the organization",
            "roleIds": ["org-employee"],
        }
    )

    invited_contact = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-temp@test.com",
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
            "userNames": ["e2e-test-corporate-temp@test.com"],
        }
    )

    auth.clear_token()

    assert invitation_result["succeeded"] == True, "User was not invited"
    assert invited_contact is not None, "Invited contact was not found"
    assert invited_contact["status"] == "Invited", "Invited contact status is not Invited"
