import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import EditAddressModal
from page_objects.pages import CartPage, CheckoutPaymentPage, CheckoutShippingPage
from playwright.sync_api import Page, expect
from tests.constants import TEST_CART_ADDRESS

_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3
_FIXED_RATE_GROUND = f"FixedRate_Ground"
_MANUAL_PAYMENT_METHOD = "DefaultManualPaymentMethod"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Payment method (E2E)")
@allure.title("Select a manual payment method on single-page checkout")
def test_checkout_payment_method_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and submit a shipping address"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        edit_address_modal = EditAddressModal(root=page.locator("body"))
        expect(edit_address_modal.edit_address_modal).to_be_visible()
        edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
        edit_address_modal.submit_button.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()

    with allure.step(f"Pick shipping method '{_FIXED_RATE_GROUND}' and verify payment section appears"):
        cart_page.shipping_details_section.select_shipping_method(code=_FIXED_RATE_GROUND)
        expect(cart_page.payment_details_section.root).to_be_visible()
        expect(cart_page.payment_details_section.selected_address_label).to_be_visible()
        expect(cart_page.payment_details_section.payment_method_selector).to_be_visible()

    with allure.step(f"Select payment method '{_MANUAL_PAYMENT_METHOD}' and verify selection"):
        cart_page.payment_details_section.select_payment_method(code=_MANUAL_PAYMENT_METHOD)
        selected_payment_method = (
            cart_page.payment_details_section.find_selected_payment_method(
                code=_MANUAL_PAYMENT_METHOD
            )
        )
        expect(selected_payment_method).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Payment method (E2E)")
@allure.title("Select a manual payment method on multi-step checkout")
def test_checkout_payment_method_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Submit shipping address on the shipping page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        edit_address_modal = EditAddressModal(root=page.locator("body"))
        expect(edit_address_modal.edit_address_modal).to_be_visible()
        edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
        edit_address_modal.submit_button.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_contain_text(str(TEST_CART_ADDRESS.line1))

    with allure.step(f"Pick shipping method '{_FIXED_RATE_GROUND}' and proceed to billing"):
        shipping_page.shipping_details_section.select_shipping_method(
            code=_FIXED_RATE_GROUND
        )
        expect(shipping_page.billing_button).to_be_visible()
        expect(shipping_page.billing_button).to_be_enabled()
        shipping_page.billing_button.click()

    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    with allure.step("Verify the payment page exposes billing/payment sections"):
        expect(payment_page.payment_details_section.root).to_be_visible()
        expect(
            payment_page.payment_details_section.billing_address_equals_shipping_checkbox
        ).to_be_visible()
        expect(payment_page.payment_details_section.selected_address_label).to_be_visible()
        expect(payment_page.payment_details_section.selected_address_label).to_contain_text(
            str(TEST_CART_ADDRESS.line1)
        )
        expect(payment_page.payment_details_section.payment_method_selector).to_be_visible()

    with allure.step(f"Select payment method '{_MANUAL_PAYMENT_METHOD}' and verify selection"):
        payment_page.payment_details_section.select_payment_method(
            code=_MANUAL_PAYMENT_METHOD
        )
        selected_payment_method = (
            payment_page.payment_details_section.find_selected_payment_method(
                code=_MANUAL_PAYMENT_METHOD
            )
        )
        expect(selected_payment_method).to_be_visible()
        expect(payment_page.review_order_button).to_be_visible()
        expect(payment_page.review_order_button).to_be_enabled()
