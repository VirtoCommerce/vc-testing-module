import allure

from tests_graphql.operations.request_registration.request_registration_operations import (
    RequestRegistrationOperations,
)


@allure.title("Register Customer (GraphQL)")
def test_register_customer(graphql_client):
    request_registration_operations = RequestRegistrationOperations(graphql_client)

    request_registration_operations.register_customer()
    request_registration_operations.clean_up_test_user()
    request_registration_operations.clean_up_test_customer()
