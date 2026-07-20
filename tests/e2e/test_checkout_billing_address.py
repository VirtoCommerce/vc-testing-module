import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import EditAddressModal, SelectAddressModal
from page_objects.pages import CartPage, CheckoutPaymentPage, CheckoutShippingPage
from playwright.sync_api import Page, expect
from tests.constants import TEST_CART_ADDRESS

_USERNAME = "acme_store_employee_1@acme.com"
_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3
_FIXED_RATE_GROUND = "FixedRate_Ground"
_ADDRESS_FRAGMENT = "742 Evergreen Terrace"
_FILTER_COUNTRY = "United States of America"
_FILTER_REGION = "North Carolina"
_FILTER_CITY = "Morrisville"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Billing address mirrors shipping address on single-page checkout")
def test_checkout_billing_address_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and submit a shipping address"):
        cart_page.navigate()
        cart_page.shipping_details_section.shipping_switcher.click()
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        edit_address_modal = EditAddressModal(
            root=page.locator("[data-test-id='edit-address-modal']")
        )
        edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
        edit_address_modal.submit_button.click()

    with allure.step("Verify billing address mirrors shipping address"):
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
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Billing address mirrors shipping address on multi-step checkout")
def test_checkout_billing_address_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Submit a shipping address on the shipping page"):
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

    with allure.step(f"Pick shipping method '{_FIXED_RATE_GROUND}' and continue to billing"):
        shipping_page.shipping_details_section.select_shipping_method(
            code=_FIXED_RATE_GROUND
        )
        expect(shipping_page.billing_button).to_be_visible()
        expect(shipping_page.billing_button).to_be_enabled()
        shipping_page.billing_button.click()

    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    with allure.step("Verify billing address on the payment page mirrors shipping"):
        expect(payment_page.payment_details_section.root).to_be_visible()
        expect(
            payment_page.payment_details_section.billing_address_equals_shipping_checkbox
        ).to_be_visible()
        expect(payment_page.payment_details_section.selected_address_label).to_be_visible()
        expect(payment_page.payment_details_section.selected_address_label).to_contain_text(
            str(TEST_CART_ADDRESS.line1)
        )


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country on single-page checkout")
def test_checkout_filter_billing_address_by_country_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and pick a saved shipping address"):
        cart_page.navigate()
        cart_page.shipping_details_section.shipping_switcher.click()
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()

    with allure.step("Open a separate billing address selection"):
        payment = cart_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}' and verify chip"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country and region on single-page checkout")
def test_checkout_filter_billing_address_by_region_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and pick a saved shipping address"):
        cart_page.navigate()
        cart_page.shipping_details_section.shipping_switcher.click()
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()

    with allure.step("Open a separate billing address selection"):
        payment = cart_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        billing_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        cart_page.click_outside()
        region_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country, region and city on single-page checkout")
def test_checkout_filter_billing_address_by_city_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and pick a saved shipping address"):
        cart_page.navigate()
        cart_page.shipping_details_section.shipping_switcher.click()
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()

    with allure.step("Open a separate billing address selection"):
        payment = cart_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        billing_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        cart_page.click_outside()
        region_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Apply city filter '{_FILTER_CITY}'"):
        billing_modal.city_filter_selector.select_item_by_name(name=_FILTER_CITY)
        cart_page.click_outside()
        city_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region/city filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country on multi-step checkout")
def test_checkout_filter_billing_address_by_country_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Pick a saved shipping address and continue to billing"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()
        shipping_page.shipping_details_section.select_shipping_method(code=_FIXED_RATE_GROUND)
        expect(shipping_page.billing_button).to_be_enabled()
        shipping_page.billing_button.click()

    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    with allure.step("Open a separate billing address selection"):
        payment = payment_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}' and verify chip"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        payment_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country and region on multi-step checkout")
def test_checkout_filter_billing_address_by_region_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Pick a saved shipping address and continue to billing"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()
        shipping_page.shipping_details_section.select_shipping_method(code=_FIXED_RATE_GROUND)
        expect(shipping_page.billing_button).to_be_enabled()
        shipping_page.billing_button.click()

    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    with allure.step("Open a separate billing address selection"):
        payment = payment_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        payment_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        billing_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        payment_page.click_outside()
        region_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Billing address (E2E)")
@allure.title("Filter saved billing addresses by country, region and city on multi-step checkout")
def test_checkout_filter_billing_address_by_city_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Pick a saved shipping address and continue to billing"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        shipping_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(shipping_modal.root).to_be_visible()
        shipping_modal.find_address(text=_ADDRESS_FRAGMENT).click()
        expect(shipping_modal.ok_button).to_be_enabled()
        shipping_modal.ok_button.click()
        expect(shipping_modal.root).not_to_be_visible()
        shipping_page.shipping_details_section.select_shipping_method(code=_FIXED_RATE_GROUND)
        expect(shipping_page.billing_button).to_be_enabled()
        shipping_page.billing_button.click()

    payment_page = CheckoutPaymentPage(global_settings=global_settings, page=page)
    with allure.step("Open a separate billing address selection"):
        payment = payment_page.payment_details_section
        expect(payment.root).to_be_visible()
        payment.uncheck_billing_equals_shipping()
        payment.select_address_button.click()
        billing_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(billing_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        billing_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        payment_page.click_outside()
        country_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        billing_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        payment_page.click_outside()
        region_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Apply city filter '{_FILTER_CITY}'"):
        billing_modal.city_filter_selector.select_item_by_name(name=_FILTER_CITY)
        payment_page.click_outside()
        city_chip = billing_modal.find_applied_filter_chip_by_name(name=_FILTER_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region/city filter"):
        expect(billing_modal.addresses.first).to_be_visible()
        expect(billing_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()
