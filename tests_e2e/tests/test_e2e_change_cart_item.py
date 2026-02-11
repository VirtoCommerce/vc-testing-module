import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage


@pytest.mark.e2e
def test_e2e_change_cart_item(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    dataset: dict[str, Any],
    page: Page,
):
    print(f"{os.linesep}Running E2E test to change cart item...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    product = dataset["products"][14]

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    auth.set_local_storage_user_id(page, user["id"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product["code"])

    assert (
        line_item is not None
    ), f"Line item with SKU {product['code']} not found in cart."

    if config["PRODUCT_QUANTITY_CONTROL"] == "stepper":
        line_item.quantity_stepper_component.increment_button.click()
    elif config["PRODUCT_QUANTITY_CONTROL"] == "button":
        line_item.add_to_cart_component.quantity_input.fill("3")

    if config["PRODUCT_QUANTITY_CONTROL"] == "stepper":
        expect(line_item.quantity_stepper_component.quantity_input).to_have_value("3")
    elif config["PRODUCT_QUANTITY_CONTROL"] == "button":
        expect(line_item.add_to_cart_component.quantity_input).to_have_value("3")

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
