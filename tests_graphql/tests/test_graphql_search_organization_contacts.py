import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.contact.contact_operations import ContactOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@allure.title("Search organization contacts by name (GraphQL)")
def test_search_organization_contacts_by_name(user_service, graphql_client):
    print(f"{os.linesep}Running test to search organization contacts by name...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="Corporate 1"
    )

    user_service.sign_out()

    assert organization_contacts["contacts"]["totalCount"] > 0, "Organization contacts not found"


@allure.title("Search organization contacts by email (GraphQL)")
def test_search_organization_contacts_by_email(user_service, graphql_client):
    print(f"{os.linesep}Running test to search organization contacts by email...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-10@test.com",
    )

    user_service.sign_out()

    assert organization_contacts["contacts"]["totalCount"] > 0, "Organization contacts not found"
