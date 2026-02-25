import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CategoryPage


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
def test_e2e_category_add_product_to_cart_with_add_to_cart_button(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to add product to a cart from category page with add to cart button...",
        end=" ",
    )

    category = dataset["categories"][0]
    product = dataset["products"][1]
    quantity_to_add = "2"

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_me()

    auth.set_local_storage_user_id(page, user["id"])

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku_grid(product["code"])
    product_card.add_to_cart_component.quantity_input.fill(quantity_to_add)
    product_card.add_to_cart_component.add_to_cart_text_button.click()

    expect(product_card.count_in_cart_label, "Count in cart label is not visible").to_be_visible()
    expect(
        product_card.count_in_cart_label, "Count in cart label is not equal to product quantity to add"
    ).to_have_text(quantity_to_add)

    cart_page = CartPage(config, page)
    cart_page.navigate()
    page.wait_for_load_state("networkidle")

    cart = cart_operations.get_cart(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code="USD",
        culture_name="en-US",
    )

    try:
        line_item = cart_page.get_line_item_by_sku(product["code"])

        assert line_item.sku == product["code"], f"Line item sku is not equal to product sku: {product['code']}"
        assert (
            line_item.add_to_cart_component.quantity_input.input_value() == quantity_to_add
        ), f"Line item quantity is not equal to product quantity to add: {quantity_to_add}"
    finally:
        cart_operations.remove_cart(
            payload={
                "cartId": cart["id"],
                "userId": user["id"],
            }
        )


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
def test_e2e_category_add_product_to_cart_with_quantity_stepper(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to add product to cart from category page with quantity stepper...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]
    product = dataset["products"][1]
    quantity_to_add = 2

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_me()

    auth.set_local_storage_user_id(page, user["id"])

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku_grid(product["code"])
    product_card.quantity_stepper_component.increment_button.click()
    product_card.quantity_stepper_component.increment_button.click()

    expect(
        product_card.quantity_stepper_component.quantity_input,
        f"Quantity input is not equal to {quantity_to_add}",
    ).to_have_value(str(quantity_to_add))
    expect(product_card.count_in_cart_label, "Count in cart label is not visible").to_be_visible()
    expect(
        product_card.count_in_cart_label, "Count in cart label is not equal to product quantity to add"
    ).to_have_text(str(quantity_to_add))

    cart_page = CartPage(config, page)
    cart_page.navigate()
    page.wait_for_load_state("networkidle")

    cart = cart_operations.get_cart(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code="USD",
        culture_name="en-US",
    )

    try:
        line_item = cart_page.get_line_item_by_sku(product["code"])

        assert line_item.sku == product["code"], f"Line item sku is not equal to product sku: {product['code']}"
        expect(
            line_item.quantity_stepper_component.quantity_input,
            f"Line item quantity is not equal to product quantity to add: {quantity_to_add}",
        ).to_have_value(str(quantity_to_add))
    finally:
        cart_operations.remove_cart(
            payload={
                "cartId": cart["id"],
                "userId": user["id"],
            }
        )
