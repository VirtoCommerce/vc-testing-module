import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.feature("Registration by invitation (GraphQL)")
def test_graphql_registration_by_invitation(config: dict, auth: Auth, graphql_client: GraphQLClient, webapi_client):
    print(f"{os.linesep}Running GraphQL test to register a user by invitation...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    contact_operations.invite_user(
        payload={
            "storeId": config["store_id"],
            "organizationId": user["contact"]["organizationId"],
            "emails": ["e2e-test-corporate-temp@test.com"],
            "message": "You are invited to join the organization",
            "roleIds": ["org-employee"],
        }
    )

    invited_user = user_operations.get_user_by_username("e2e-test-corporate-temp@test.com")

    token = webapi_client.get(f"/api/platform/security/users/{invited_user['id']}/generatePasswordResetToken")

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
