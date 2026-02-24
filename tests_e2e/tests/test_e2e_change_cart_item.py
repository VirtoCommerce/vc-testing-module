import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CategoryPage


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
def test_e2e_change_cart_item_stepper(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    dataset: dict[str, Any],
    page: Page,
):
    print(f"{os.linesep}Running E2E test to change cart item with stepper...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    product = dataset["products"][1]

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
    line_item.quantity_stepper_component.increment_button.click()

    expect(line_item.quantity_stepper_component.quantity_input).to_have_value("3")

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
def test_e2e_change_cart_item_button(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    dataset: dict[str, Any],
    page: Page,
):
    print(f"{os.linesep}Running E2E test to change cart item with button...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    product = dataset["products"][1]

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
    line_item.add_to_cart_component.quantity_input.fill("3")

    expect(line_item.add_to_cart_component.quantity_input).to_have_value("3")

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
