import allure

from graphql_requests.delete_users.delete_users_request import RequestDeleteUsers
from graphql_requests.delete_contact.delete_contact_request import RequestDeleteContact
from graphql_requests.request_registration.request_registration_request import RequestRegistrationRequest

@allure.title("Successfull Register Organization (GraphQL)")
def test_register_organization(graphql_client):
    print("Successfull Register Organization (GraphQL)")

    email = "e2e-gql-test@test.com"

    requestRegistrationRequest = RequestRegistrationRequest(graphql_client)

    requestRegistrationResult = requestRegistrationRequest.execute(
        store_id="B2B-store",
        email=email,
        password="Password1!",
        first_name="John",
        last_name="Doe",
        organization_name="E2E Test Organization"
    )

    succeeded = requestRegistrationResult["requestRegistration"]["result"]["succeeded"]
    account = requestRegistrationResult["requestRegistration"]["account"]
    contact = requestRegistrationResult["requestRegistration"]["contact"]
    organization = requestRegistrationResult["requestRegistration"]["organization"]

    # Clean up test user
    deleteUsersRequest = RequestDeleteUsers(graphql_client)
    deleteUsersRequest.execute([email])

    # Clean up test contact and organization
    deleteContactRequest = RequestDeleteContact(graphql_client)
    deleteContactRequest.execute(contact["id"])
    deleteContactRequest.execute(organization["id"])

    assert succeeded is True
    assert account is not None
    assert contact is not None
    assert organization is not None