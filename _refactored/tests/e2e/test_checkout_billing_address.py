import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.components import EditAddressModal
from page_objects.pages import CartPage, CheckoutPaymentPage, CheckoutShippingPage
from tests.constants import TEST_CART_ADDRESS

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3
_FIXED_RATE_GROUND = "FixedRate_Ground"
_GROUND = "Ground"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_billing_address_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.shipping_switcher.click()
    cart_page.shipping_details_section.shipping_address_section.select_address_button.click()

    edit_address_modal = EditAddressModal(
        root=page.locator("[data-test-id='edit-address-modal']")
    )
    edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
    edit_address_modal.submit_button.click()

    expect(cart_page.payment_details_section.root).to_be_visible()
    expect(
        cart_page.payment_details_section.billing_address_equals_shipping_checkbox
    ).to_be_visible()
    expect(cart_page.payment_details_section.selected_address_label).to_be_visible()
    expect(cart_page.payment_details_section.selected_address_label).to_contain_text(
        str(TEST_CART_ADDRESS.line1)
    )


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_billing_address_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_enabled()

    cart_page.checkout_button.click()
    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    expect(shipping_page.shipping_details_section.root).to_be_visible()

    shipping_page.shipping_details_section.shipping_switcher.click()
    shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
    edit_address_modal = EditAddressModal(
        root=page.locator("[data-test-id='edit-address-modal']")
    )
    edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
    edit_address_modal.submit_button.click()
    expect(
        shipping_page.shipping_details_section.shipping_address_section.current_address_label
    ).to_be_visible()
    expect(
        shipping_page.shipping_details_section.shipping_address_section.current_address_label
    ).to_contain_text(str(TEST_CART_ADDRESS.line1))

    shipping_page.shipping_details_section.select_shipping_method(
        code=_FIXED_RATE_GROUND
    )
    expect(shipping_page.billing_button).to_be_visible()
    expect(shipping_page.billing_button).to_be_enabled()

    shipping_page.billing_button.click()
    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    expect(payment_page.payment_details_section.root).to_be_visible()
    expect(
        payment_page.payment_details_section.billing_address_equals_shipping_checkbox
    ).to_be_visible()
    expect(payment_page.payment_details_section.selected_address_label).to_be_visible()
    expect(payment_page.payment_details_section.selected_address_label).to_contain_text(
        str(TEST_CART_ADDRESS.line1)
    )
