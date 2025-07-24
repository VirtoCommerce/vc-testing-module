import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1, TEST_CUSTOMER_ADDRESS_2
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.title("Update organization address (GraphQL)")
def test_update_organization_address(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update organization address...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    contact = contact_operations.update_contact_addresses(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [TEST_CUSTOMER_ADDRESS_1]}
    )

    added_address = contact["addresses"]["items"][0]

    updated_contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [
                {**added_address, "line1": "1234 Pine Drive"},
            ],
        }
    )

    updated_address = updated_contact["addresses"]["items"][0]

    # Test teardown

    contact_operations.delete_contact_address(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [updated_address]}
    )

    auth.clear_token()

    assert updated_address is not None, "Updated address is None"
    assert updated_address["line1"] == "1234 Pine Drive", "Contact address line1 is not updated"
