import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.feature("Lock organization contact (GraphQL)")
def test_lock_organization_contact(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to lock organization contact...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    dataset_user = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-administrator"
    )

    auth.authenticate(
        dataset_user["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    organization_contact_to_lock = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="ACME Purchasing Agent 3",
    )["contacts"]["items"][0]

    locked_contact = contact_operations.lock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    unlocked_contact = contact_operations.unlock_organization_contact(
        payload={
            "userId": organization_contact_to_lock["id"],
        }
    )

    auth.clear_token()

    assert locked_contact["status"] == "Locked", "Contact is not locked"
    assert unlocked_contact["status"] == "Approved", "Contact is not unlocked"
