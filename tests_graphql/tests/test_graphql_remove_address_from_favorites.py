import allure, os, pytest
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.title("Add address to favorites (GraphQL)")
def test_add_address_to_favorites(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add address to favorites...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    contact = contact_operations.update_contact_addresses(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [TEST_CUSTOMER_ADDRESS_1]}
    )

    added_address = contact["addresses"]["items"][0]

    contact_operations.add_address_to_favorites(payload={"addressId": added_address["id"]})

    contact_operations.remove_address_from_favorites(payload={"addressId": added_address["id"]})

    organization = contact_operations.fetch_organization_addresses(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
    )

    favorite_address = next((address for address in organization["addresses"]["items"] if address["isFavorite"]), None)

    # Test teardown

    contact_operations.delete_contact_address(
        payload={"memberId": user["contact"]["organizationId"], "addresses": [added_address]}
    )

    auth.clear_token()

    assert favorite_address is None, "Favorite address is not removed"
