import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.title("Search organization contacts by name (GraphQL)")
def test_search_organization_contacts_by_name(auth, graphql_client):
    print(f"{os.linesep}Running test to search organization contacts by name...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="Employee"
    )

    auth.clear_token()

    assert organization_contacts["contacts"]["totalCount"] > 0, "Organization contacts not found"


@pytest.mark.graphql
@allure.title("Search organization contacts by email (GraphQL)")
def test_search_organization_contacts_by_email(auth, graphql_client):
    print(f"{os.linesep}Running test to search organization contacts by email...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-employee-1@e2e-contoso.com",
    )

    auth.clear_token()

    assert organization_contacts["contacts"]["totalCount"] > 0, "Organization contacts not found"
