import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.e2e
def test_e2e_checkout_multi_step_switch_shipping_option(
    config: Config,
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
):
    if config["CHECKOUT_MODE"] == "single-page":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to switch shipping option in multi-step checkout...",
        end=" ",
    )

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

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()

    expect(page).to_have_url(
        checkout_shipping_page.url
    ), "Checkout shipping page is not loaded"
    expect(
        checkout_shipping_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher
    ).to_be_visible(), "Pickup delivery option switcher is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_delivery_option_switcher
    ).to_be_visible(), "Shipping delivery option switcher is not visible"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "pickup"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section
    ).to_be_visible(), "Pickup point section is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector
    ).not_to_be_visible(), "Shipping method selector is visible"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "shipping"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section
    ).not_to_be_visible(), "Pickup point section is visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
def test_e2e_checkout_single_page_switch_shipping_option(
    config: Config,
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
):
    if config["CHECKOUT_MODE"] == "multi-step":
        pytest.skip(
            "Checkout mode is a multi-step, skipping test for single-page checkout"
        )

    print(
        f"{os.linesep}Running E2E test to switch shipping option in single-page checkout...",
        end=" ",
    )

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

    expect(page).to_have_url(cart_page.url), "Cart page is not loaded"
    expect(
        cart_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"
    expect(
        cart_page.shipping_details_section_component.pickup_delivery_option_switcher
    ).to_be_visible(), "Pickup delivery option switcher is not visible"
    expect(
        cart_page.shipping_details_section_component.shipping_delivery_option_switcher
    ).to_be_visible(), "Shipping delivery option switcher is not visible"

    cart_page.shipping_details_section_component.switch_delivery_option("pickup")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section
    ).to_be_visible(), "Pickup point section is not visible"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).not_to_be_visible(), "Shipping method selector is visible"

    cart_page.shipping_details_section_component.switch_delivery_option("shipping")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section
    ).not_to_be_visible(), "Pickup point section is visible"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
