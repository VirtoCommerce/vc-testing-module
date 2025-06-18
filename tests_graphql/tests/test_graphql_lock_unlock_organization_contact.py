import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.feature("Lock organization contact (GraphQL)")
def test_lock_organization_contact(auth, graphql_client):
    print(f"{os.linesep}Running test to lock organization contact...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contact_to_lock = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-10@test.com",
    )["contacts"]["items"][0]

    locked_contact = contact_operations.lock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    auth.clear_token()

    assert locked_contact["status"] == "Locked", "Contact is not locked"


@pytest.mark.graphql
@allure.feature("Unlock organization contact (GraphQL)")
def test_unlock_organization_contact(auth, graphql_client):
    print(f"{os.linesep}Running test to lock organization contact...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contact_to_lock = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-10@test.com",
    )["contacts"]["items"][0]

    unlocked_contact = contact_operations.unlock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    auth.clear_token()

    assert unlocked_contact["status"] == "Approved", "Contact is not unlocked"
