import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, SaveForLaterPage


@pytest.mark.e2e
def test_e2e_add_product_to_cart_and_save_for_later(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to add product to cart and save for later...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

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

    cart_page.save_for_later(product["code"])

    line_item = cart_page.get_line_item_by_sku(product["code"])
    expect(
        line_item.element
    ).not_to_be_visible(), f"Product {product['code']} should not be in cart"

    save_for_later_page = SaveForLaterPage(page, config)
    save_for_later_page.navigate()

    saved_item = save_for_later_page.get_line_item_by_sku(product["code"])
    expect(
        saved_item.element
    ).to_be_visible(), f"Product {product['code']} should be in saved for later"

    save_for_later_page.remove_line_item(product["code"])

    expect(
        saved_item.element
    ).not_to_be_visible(), f"Product {product['code']} should not be in saved for later"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
def test_e2e_move_product_from_saved_for_later_to_cart(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to move product from saved for later to cart...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    product = dataset["products"][1]
    product_quantity = 3

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": product_quantity,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.save_for_later(product["code"])

    line_item = cart_page.get_line_item_by_sku(product["code"])
    expect(
        line_item.element
    ).not_to_be_visible(), f"Product {product['code']} should not be in cart"

    save_for_later_page = SaveForLaterPage(page, config)
    save_for_later_page.navigate()

    saved_item = save_for_later_page.get_line_item_by_sku(product["code"])
    expect(
        saved_item.element
    ).to_be_visible(), f"Product {product['code']} should be in saved for later"

    saved_item.add_to_cart_component.add_to_cart_text_button.click()
    page.locator(".vc-dialog-footer button.vc-button--solid--primary").click()

    expect(
        saved_item.element
    ).to_be_visible(), f"Product {product['code']} should be in saved for later"

    save_for_later_page.remove_line_item(product["code"])

    expect(
        saved_item.element
    ).not_to_be_visible(), f"Product {product['code']} should not be in saved for later"

    cart_page.navigate()
    line_item = cart_page.get_line_item_by_sku(product["code"])
    expect(
        line_item.element
    ).to_be_visible(), f"Product {product['code']} should be in cart"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
