import os

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_customer import TEST_CUSTOMER
from test_data.test_organization import TEST_ORGANIZATION
from test_data.test_user import TEST_ADMIN_USER, TEST_USER


@pytest.mark.graphql
@allure.title("Register customer (GraphQL)")
def test_register_customer(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to register customer...", end=" ")

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

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

    auth.clear_token()

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"] is not None
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"] is None


@pytest.mark.graphql
@allure.title("Register organization (GraphQL)")
def test_register_organization(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to register organization...", end=" ")

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

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

    auth.clear_token()

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"]["id"] is not None
