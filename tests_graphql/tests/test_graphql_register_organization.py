import allure

from tests_graphql.operations.request_registration.request_registration_operations import (
    RequestRegistrationOperations,
)


@allure.title("Register Organization (GraphQL)")
def test_register_organization(graphql_client):
    request_registration_operations = RequestRegistrationOperations(graphql_client)

    request_registration_operations.register_organization()
    request_registration_operations.clean_up_test_user()
    request_registration_operations.clean_up_test_customer()
    request_registration_operations.clean_up_test_organization()
