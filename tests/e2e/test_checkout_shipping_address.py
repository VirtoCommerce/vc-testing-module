import pytest
from core.global_settings import GlobalSettings
from page_objects.components import EditAddressModal, SelectAddressModal
from page_objects.pages import CartPage, CheckoutShippingPage
from playwright.sync_api import Page, expect
from tests.constants import TEST_CART_ADDRESS

_USERNAME = "acme_store_employee_1@acme.com"
_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3
_ADDRESS_FRAGMENT = "742 Evergreen Terrace"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_add_shipping_address_single_page(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.shipping_details_section.root).to_be_visible()

    cart_page.shipping_details_section.shipping_switcher.click()
    expect(cart_page.shipping_details_section.shipping_address_section.root).to_be_visible()
    expect(cart_page.shipping_details_section.shipping_address_section.select_address_button).to_be_visible()

    cart_page.shipping_details_section.shipping_address_section.select_address_button.click()

    edit_address_modal = EditAddressModal(root=page.locator("[data-test-id='edit-address-modal']"))
    expect(edit_address_modal.root).to_be_visible()

    edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
    expect(edit_address_modal.submit_button).to_be_enabled()

    edit_address_modal.submit_button.click()
    expect(edit_address_modal.root).not_to_be_visible()
    expect(cart_page.shipping_details_section.shipping_address_section.current_address_label).to_be_visible()
    expect(cart_page.shipping_details_section.shipping_address_section.current_address_label).to_contain_text(
        str(TEST_CART_ADDRESS.line1)
    )


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_select_shipping_address_single_page(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.shipping_details_section.root).to_be_visible()

    cart_page.shipping_details_section.shipping_switcher.click()
    expect(cart_page.shipping_details_section.shipping_address_section.root).to_be_visible()
    expect(cart_page.shipping_details_section.shipping_address_section.select_address_button).to_be_visible()

    cart_page.shipping_details_section.shipping_address_section.select_address_button.click()

    select_address_modal = SelectAddressModal(root=page.locator("[data-test-id='select-address-modal']"))
    expect(select_address_modal.root).to_be_visible()

    address = select_address_modal.find_address(text=_ADDRESS_FRAGMENT)
    expect(address).to_be_visible()

    address.click()
    expect(select_address_modal.ok_button).to_be_enabled()

    select_address_modal.ok_button.click()
    expect(select_address_modal.root).not_to_be_visible()
    expect(cart_page.shipping_details_section.shipping_address_section.current_address_label).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_add_shipping_address_multi_step(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_enabled()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    expect(shipping_page.shipping_details_section.root).to_be_visible()

    shipping_page.shipping_details_section.shipping_switcher.click()
    expect(shipping_page.shipping_details_section.shipping_address_section.root).to_be_visible()

    shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()

    edit_address_modal = EditAddressModal(root=page.locator("[data-test-id='edit-address-modal']"))
    expect(edit_address_modal.root).to_be_visible()

    edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
    expect(edit_address_modal.submit_button).to_be_enabled()

    edit_address_modal.submit_button.click()
    expect(edit_address_modal.root).not_to_be_visible()
    expect(shipping_page.shipping_details_section.shipping_address_section.current_address_label).to_be_visible()
    expect(shipping_page.shipping_details_section.shipping_address_section.current_address_label).to_contain_text(
        str(TEST_CART_ADDRESS.line1)
    )


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_select_shipping_address_multi_step(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_enabled()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    expect(shipping_page.shipping_details_section.root).to_be_visible()

    shipping_page.shipping_details_section.shipping_switcher.click()
    expect(shipping_page.shipping_details_section.shipping_address_section.root).to_be_visible()

    shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()

    select_address_modal = SelectAddressModal(root=page.locator("[data-test-id='select-address-modal']"))
    expect(select_address_modal.root).to_be_visible()

    address = select_address_modal.find_address(text=_ADDRESS_FRAGMENT)
    expect(address).to_be_visible()

    address.click()
    expect(select_address_modal.ok_button).to_be_enabled()

    select_address_modal.ok_button.click()
    expect(select_address_modal.root).not_to_be_visible()
    expect(shipping_page.shipping_details_section.shipping_address_section.current_address_label).to_be_visible()
