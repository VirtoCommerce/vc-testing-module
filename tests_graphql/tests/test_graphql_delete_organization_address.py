import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_address import TEST_CUSTOMER_ADDRESS, TEST_CUSTOMER_ADDRESS_1
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.title("Delete organization address (GraphQL)")
def test_delete_organization_address(auth, graphql_client):
    print(f"{os.linesep}Running test to delete organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    contact = contact_operations.update_contact_addresses(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [TEST_CUSTOMER_ADDRESS]}
    )

    added_address = contact["addresses"]["items"][0]

    updated_contact = contact_operations.delete_contact_address(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [added_address]}
    )

    auth.clear_token()

    assert len(updated_contact["addresses"]["items"]) == 0, "Contact addresses are not deleted"
