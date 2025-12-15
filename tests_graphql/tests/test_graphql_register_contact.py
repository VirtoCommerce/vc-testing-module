import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Register customer (GraphQL)")
def test_register_customer(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to register customer...", end=" ")

    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-administrator"
    )

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    temp_email = "some-email@acme.com"

    create_contact_result = contact_operations.create_contact(
        payload={
            "storeId": config["STORE_ID"],
            "account": {
                "username": temp_email,
                "email": temp_email,
                "password": config["USERS_PASSWORD"],
            },
            "contact": {
                "firstName": "ACME",
                "lastName": "Customer",
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
            "userNames": [temp_email],
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
def test_register_organization(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to register organization...", end=" ")

    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-administrator"
    )

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    temp_email = "some-email@acme.com"

    create_contact_result = contact_operations.create_contact(
        payload={
            "storeId": config["STORE_ID"],
            "account": {
                "username": temp_email,
                "email": temp_email,
                "password": config["USERS_PASSWORD"],
            },
            "contact": {
                "firstName": "ACME",
                "lastName": "Customer",
            },
            "organization": {
                "name": "Temp Organization",
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
            "userNames": [temp_email],
        }
    )

    auth.clear_token()

    assert create_contact_result["result"]["succeeded"] is True
    assert create_contact_result["account"]["id"] is not None
    assert create_contact_result["contact"]["id"] is not None
    assert create_contact_result["organization"]["id"] is not None
