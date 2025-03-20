from tests_graphql.test_data.test_store import TEST_STORE as test_store
from tests_graphql.test_data.test_user import TEST_USER as test_user
from tests_graphql.test_data.test_customer import TEST_CUSTOMER as test_customer
from tests_graphql.test_data.test_organization import TEST_ORGANIZATION as test_organization
from graphql_requests.delete_users.delete_users_request import RequestDeleteUsers
from graphql_requests.delete_contact.delete_contact_request import RequestDeleteContact
from graphql_requests.request_registration.request_registration_request import RequestRegistrationRequest


class CustomerRegistrationOperations:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client
        self.requestRegistrationRequest = RequestRegistrationRequest(self.graphql_client)
        self.contact_id = None
        self.organization_id = None

    def register_organization(self):
        result = self.requestRegistrationRequest.execute(
            store_id=test_store["id"],
            email=test_user["email"],
            password=test_user["password"],
            first_name=test_customer["firstName"],
            last_name=test_customer["lastName"],
            organization_name=test_organization["name"],
        )

        self.contact_id = result["requestRegistration"]["contact"]["id"]
        self.organization_id = result["requestRegistration"]["organization"]["id"]

        assert result["requestRegistration"]["result"]["succeeded"] is True
        assert result["requestRegistration"]["account"] is not None
        assert result["requestRegistration"]["contact"] is not None
        assert result["requestRegistration"]["organization"] is not None

    def clean_up_test_user(self):
        deleteUsersRequest = RequestDeleteUsers(self.graphql_client)
        deleteUsersRequest.execute([test_user["email"]])

    def clean_up_test_customer(self):
        deleteContactRequest = RequestDeleteContact(self.graphql_client)
        deleteContactRequest.execute(self.contact_id)

    def clean_up_test_organization(self):
        deleteContactRequest = RequestDeleteContact(self.graphql_client)
        deleteContactRequest.execute(self.organization_id)
