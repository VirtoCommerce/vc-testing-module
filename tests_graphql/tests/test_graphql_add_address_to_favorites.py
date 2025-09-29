import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add address to favorites (GraphQL)")
def test_add_address_to_favorites(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to add address to favorites...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["users_password"])

    user = user_operations.get_me()

    temp_address = {
        "addressType": 3,
        "city": "Austin",
        "countryCode": "USA",
        "countryName": "United States of America",
        "line1": "1600 Hollow Creek Drive",
        "postalCode": "78704",
        "regionId": "TX",
        "regionName": "Texas",
    }

    contact = contact_operations.update_contact_addresses(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [temp_address],
        }
    )

    added_address = next(
        (
            address
            for address in contact["addresses"]["items"]
            if address["city"] == temp_address["city"]
            and address["countryCode"] == temp_address["countryCode"]
            and address["countryName"] == temp_address["countryName"]
            and address["line1"] == temp_address["line1"]
            and address["postalCode"] == temp_address["postalCode"]
            and address["regionId"] == temp_address["regionId"]
            and address["regionName"] == temp_address["regionName"]
        ),
        None,
    )

    contact_operations.add_address_to_favorites(
        payload={"addressId": added_address["id"]}
    )

    organization = contact_operations.fetch_organization_addresses(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
    )

    favorite_address = next(
        (
            address
            for address in organization["addresses"]["items"]
            if address["isFavorite"]
        ),
        None,
    )

    # Test teardown

    contact_operations.delete_contact_address(
        payload={
            "memberId": user["contact"]["organizationId"],
            "addresses": [added_address],
        }
    )

    auth.clear_token()

    assert favorite_address is not None, "Favorite address is None"
    assert (
        favorite_address["id"] == added_address["id"]
    ), "Favorite address is not the added address"
