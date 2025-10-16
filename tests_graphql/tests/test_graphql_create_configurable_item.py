import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.ignore
@pytest.mark.graphql
@allure.title("Create configurable item (GraphQL)")
def test_create_configurable_item(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to create configurable item...", end=" ")

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    base_product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        id=dataset["products"][0]["id"],
        culture_name=dataset["languages"][0]["allowedValues"][0],
        currency_code=dataset["currencies"][0]["code"],
    )

    product_configuration = products_operations.get_product_configuration(
        store_id=config["store_id"],
        user_id=user["id"],
        configurable_product_id=dataset["products"][0]["id"],
        culture_name=dataset["languages"][0]["allowedValues"][0],
        currency_code=dataset["currencies"][0]["code"],
    )

    configuration_sections = []

    for section in product_configuration["configurationSections"]:
        configuration_section = {
            "sectionId": section["id"],
            "type": section["type"],
        }

        if section["type"] == "Product":
            configuration_section["option"] = {
                "productId": section["options"][0]["product"]["id"],
                "quantity": section["options"][0]["quantity"],
            }
        elif section["type"] == "Text":
            configuration_section["customText"] = "Some Text"
        elif section["type"] == "File":
            configuration_section["fileUrls"] = [
                config["frontend_base_url"],
            ]

        configuration_sections.append(configuration_section)

    configured_line_item = products_operations.create_configured_line_item(
        payload={
            "storeId": config["store_id"],
            "configurableProductId": dataset["products"][0]["id"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "currencyCode": dataset["currencies"][0]["code"],
            "configurationSections": configuration_sections,
        }
    )

    assert base_product["isConfigurable"] == True, "Base product is not configurable"
    assert (
        configured_line_item["quantity"] == 1
    ), "Configured line item quantity is not set"
    assert (
        configured_line_item["product"]["id"] == base_product["id"]
    ), "Configured line item product id is not set"
