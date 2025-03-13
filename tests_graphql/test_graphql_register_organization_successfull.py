import allure

from tests_graphql.pages.customer_registration.customer_registration_page import CustomerRegistrationPage

@allure.title("Successfull Register Organization (GraphQL)")
def test_register_organization(graphql_client):
    customer_registration_page = CustomerRegistrationPage(graphql_client)

    customer_registration_page.register_organization()
    customer_registration_page.clean_up_test_user()
    customer_registration_page.clean_up_test_customer()
    customer_registration_page.clean_up_test_organization()