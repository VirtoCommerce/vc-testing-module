import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.feature("Lock organization contact (GraphQL)")
def test_lock_organization_contact(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to lock organization contact...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

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
