import allure

from tests_graphql.operations.customer_registration.customer_registration_operations import (
    CustomerRegistrationOperations,
)


@allure.title("Successfull Register Organization (GraphQL)")
def test_register_organization(graphql_client):
    customer_registration_operations = CustomerRegistrationOperations(graphql_client)

    customer_registration_operations.register_organization()
    customer_registration_operations.clean_up_test_user()
    customer_registration_operations.clean_up_test_customer()
    customer_registration_operations.clean_up_test_organization()
