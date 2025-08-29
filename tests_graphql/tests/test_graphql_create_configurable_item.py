import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_CONFIGURABLE_PRODUCT_1


@pytest.mark.graphql
@allure.title("Create configurable item (GraphQL)")
def test_create_configurable_item(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to create configurable item...", end=" ")

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    base_product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        id=TEST_CONFIGURABLE_PRODUCT_1["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
    )

    product_configuration = products_operations.get_product_configuration(
        store_id=config["store_id"],
        user_id=user["id"],
        configurable_product_id=TEST_CONFIGURABLE_PRODUCT_1["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
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
            "configurableProductId": TEST_CONFIGURABLE_PRODUCT_1["id"],
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
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
