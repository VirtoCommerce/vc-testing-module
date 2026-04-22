import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage, CheckoutShippingPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_shipping_option_switch_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.shipping_details_section.root).to_be_visible()
    expect(cart_page.shipping_details_section.shipping_switcher).to_be_visible()
    expect(cart_page.shipping_details_section.pickup_switcher).to_be_visible()

    cart_page.shipping_details_section.shipping_switcher.click()
    expect(
        cart_page.shipping_details_section.shipping_address_section.root
    ).to_be_visible()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(
        cart_page.shipping_details_section.pickup_location_section.root
    ).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_shipping_option_switch_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_enabled()

    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    expect(shipping_page.shipping_details_section.root).to_be_visible()
    expect(shipping_page.shipping_details_section.shipping_switcher).to_be_visible()
    expect(shipping_page.shipping_details_section.pickup_switcher).to_be_visible()

    shipping_page.shipping_details_section.shipping_switcher.click()
    expect(
        shipping_page.shipping_details_section.shipping_address_section.root
    ).to_be_visible()

    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(
        shipping_page.shipping_details_section.pickup_location_section.root
    ).to_be_visible()
