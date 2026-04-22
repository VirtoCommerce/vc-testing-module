import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage


@pytest.mark.e2e
def test_e2e_remove_cart_item(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
    auth: Auth,
):
    print(f"{os.linesep}Running E2E test to remove cart item...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product["code"])
    line_item.remove_button.click()

    expect(line_item.element).not_to_be_visible(), "Line item is still visible after removing"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
