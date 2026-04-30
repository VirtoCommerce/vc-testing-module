import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage, CheckoutShippingPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping option (E2E)")
@allure.title("Toggle between shipping and pickup on single-page checkout")
def test_checkout_shipping_option_switch_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and verify shipping/pickup switchers"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        expect(cart_page.shipping_details_section.shipping_switcher).to_be_visible()
        expect(cart_page.shipping_details_section.pickup_switcher).to_be_visible()

    with allure.step("Switch to shipping and verify shipping address section is shown"):
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Switch to pickup and verify pickup location section is shown"):
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(
            cart_page.shipping_details_section.pickup_location_section.root
        ).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping option (E2E)")
@allure.title("Toggle between shipping and pickup on multi-step checkout")
def test_checkout_shipping_option_switch_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Verify shipping page exposes both shipping and pickup switchers"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        expect(shipping_page.shipping_details_section.shipping_switcher).to_be_visible()
        expect(shipping_page.shipping_details_section.pickup_switcher).to_be_visible()

    with allure.step("Switch to shipping and verify shipping address section is shown"):
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Switch to pickup and verify pickup location section is shown"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(
            shipping_page.shipping_details_section.pickup_location_section.root
        ).to_be_visible()
