import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add variation to cart (GraphQL)")
def test_add_variation_to_cart(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):

    print(f"{os.linesep}Running test to add variation to cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    catalog = dataset["catalogs"][0]
    product_family_id = dataset["productVariations"][0]["mainProductId"]

    user = user_operations.get_me()

    search_variations_result_in_stock = product_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']} price.{currency}:(0 TO) productfamilyid:{product_family_id} is:product,variation availability:InStock",
    )

    variation = search_variations_result_in_stock["items"][1]["id"]

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": variation,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 1, "Items quantity is not the same"
