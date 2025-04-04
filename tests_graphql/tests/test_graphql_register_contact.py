import allure
import os
from tests_graphql.operations.contact.contact_operations import ContactOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_customer import TEST_CUSTOMER
from tests_graphql.test_data.test_organization import TEST_ORGANIZATION
from tests_graphql.test_data.test_user import TEST_USER


@allure.title("Register customer (GraphQL)")
def test_register_customer(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to register customer...", end=" ")

    contact_operations = ContactOperations(auth_token, graphql_client)
    create_contact_result = contact_operations.create_contact(
        store_id=config["store_id"],
        email=TEST_USER["email"],
        password=TEST_USER["password"],
        first_name=TEST_CUSTOMER["firstName"],
        last_name=TEST_CUSTOMER["lastName"],
    )["requestRegistration"]

    # Test teardown
    contact_operations.delete_contact(create_contact_result["contact"]["id"])

    user_operations = UserOperations(auth_token, graphql_client)
    user_operations.delete_users([TEST_USER["email"]])

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"] is not None
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"] is None


@allure.title("Register organization (GraphQL)")
def test_register_organization(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to register organization...", end=" ")

    contact_operations = ContactOperations(auth_token, graphql_client)
    create_contact_result = contact_operations.create_contact(
        store_id=config["store_id"],
        email=TEST_USER["email"],
        password=TEST_USER["password"],
        first_name=TEST_CUSTOMER["firstName"],
        last_name=TEST_CUSTOMER["lastName"],
        organization_name=TEST_ORGANIZATION["name"],
    )["requestRegistration"]

    # Test teardown
    contact_operations.delete_contact(create_contact_result["contact"]["id"])
    contact_operations.delete_contact(create_contact_result["organization"]["id"])

    user_operations = UserOperations(auth_token, graphql_client)
    user_operations.delete_users([TEST_USER["email"]])

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"]["id"] is not None
