import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.clear_cart_modal_component import ClearCartModalComponent
from tests_e2e.pages import CartPage


@pytest.mark.e2e
def test_e2e_clear_cart(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running E2E test to clear cart...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": "product-acme-laptop-hp-pavilion-16-ag0087nr",
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.clear_cart_button.click()

    clear_cart_modal = ClearCartModalComponent(
        page.locator("[data-test-id='clear-cart-modal']")
    )

    expect(clear_cart_modal.element).to_be_visible(), "Clear cart modal is not visible"

    clear_cart_modal.no_button.click()

    expect(clear_cart_modal.element).not_to_be_visible(), "Clear cart modal is visible"

    cart_page.clear_cart()

    expect(
        cart_page.clear_cart_button
    ).not_to_be_visible(), "Clear cart button is visible"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
