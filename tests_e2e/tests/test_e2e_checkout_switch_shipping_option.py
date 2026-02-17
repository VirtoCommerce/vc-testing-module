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

    product = dataset["products"][14]

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

    expect(page, "Checkout shipping page is not loaded").to_have_url(
        checkout_shipping_page.url
    )
    expect(
        checkout_shipping_page.shipping_details_section_component.element,
        "Shipping details section is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher,
        "Pickup delivery option switcher is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_delivery_option_switcher,
        "Shipping delivery option switcher is not visible",
    ).to_be_visible()

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "pickup"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section,
        "Pickup point section is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is visible",
    ).not_to_be_visible()

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "shipping"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section,
        "Pickup point section is visible",
    ).not_to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is not visible",
    ).to_be_visible()

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

    product = dataset["products"][14]

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

    expect(page, "Cart page is not loaded").to_have_url(cart_page.url)
    assert (
        cart_page.shipping_details_section_component is not None
    ), "Shipping details section component is not found"
    expect(
        cart_page.shipping_details_section_component.element,
        "Shipping details section is not visible",
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.pickup_delivery_option_switcher,
        "Pickup delivery option switcher is not visible",
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.shipping_delivery_option_switcher,
        "Shipping delivery option switcher is not visible",
    ).to_be_visible()

    cart_page.shipping_details_section_component.switch_delivery_option("pickup")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section,
        "Pickup point section is not visible",
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is visible",
    ).not_to_be_visible()

    cart_page.shipping_details_section_component.switch_delivery_option("shipping")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section,
        "Pickup point section is visible",
    ).not_to_be_visible()
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is not visible",
    ).to_be_visible()

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
