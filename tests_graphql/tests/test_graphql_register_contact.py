import allure
import os
from tests_graphql.operations.contact.contact_operations import ContactOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_customer import TEST_CUSTOMER
from tests_graphql.test_data.test_organization import TEST_ORGANIZATION
from tests_graphql.test_data.test_user import TEST_USER
from tests_graphql.test_data.test_user import TEST_ADMIN_USER


@allure.title("Register customer (GraphQL)")
def test_register_customer(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to register customer...", end=" ")

    user_service.sign_in(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    contact_operations = ContactOperations(graphql_client)
    create_contact_result = contact_operations.create_contact(
        payload={
            "storeId": config["store_id"],
            "account": {
                "username": TEST_USER["email"],
                "email": TEST_USER["email"],
                "password": TEST_USER["password"],
            },
            "contact": {
                "firstName": TEST_CUSTOMER["firstName"],
                "lastName": TEST_CUSTOMER["lastName"],
            },
        }
    )

    # Test teardown
    contact_operations.delete_contact(
        payload={
            "contactId": create_contact_result["contact"]["id"],
        }
    )

    user_operations = UserOperations(graphql_client)
    user_operations.delete_users(
        payload={
            "userNames": [TEST_USER["email"]],
        }
    )

    user_service.sign_out()

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"] is not None
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"] is None


@allure.title("Register organization (GraphQL)")
def test_register_organization(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to register organization...", end=" ")

    user_service.sign_in(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    contact_operations = ContactOperations(graphql_client)
    create_contact_result = contact_operations.create_contact(
        payload={
            "storeId": config["store_id"],
            "account": {
                "username": TEST_USER["email"],
                "email": TEST_USER["email"],
                "password": TEST_USER["password"],
            },
            "contact": {
                "firstName": TEST_CUSTOMER["firstName"],
                "lastName": TEST_CUSTOMER["lastName"],
            },
            "organization": {
                "name": TEST_ORGANIZATION["name"],
            },
        }
    )

    # Test teardown
    contact_operations.delete_contact(
        payload={
            "contactId": create_contact_result["contact"]["id"],
        }
    )
    contact_operations.delete_contact(
        payload={
            "contactId": create_contact_result["organization"]["id"],
        }
    )

    user_operations = UserOperations(graphql_client)
    user_operations.delete_users(
        payload={
            "userNames": [TEST_USER["email"]],
        }
    )

    user_service.sign_out()

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"]["id"] is not None
