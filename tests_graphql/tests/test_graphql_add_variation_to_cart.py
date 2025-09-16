import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_catalog import MIXED_CATALOG
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_2


@pytest.mark.graphql
@allure.title("Add variation to cart (GraphQL)")
def test_add_variation_to_cart(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add variation to cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    search_variations_result_in_stock = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{MIXED_CATALOG['id']} price.{TEST_CURRENCY['USD']}:(0 TO) productfamilyid:{TEST_PRODUCT_2['id']} is:product,variation availability:InStock",
    )

    variation = search_variations_result_in_stock["items"][0]

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": variation["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 1, "Items quantity is not the same"
