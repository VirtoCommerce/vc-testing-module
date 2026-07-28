import allure
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
_FILTER_COUNTRY = "United States of America"
_FILTER_REGION = "North Carolina"
_FILTER_CITY = "Morrisville"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Add a new shipping address on single-page checkout (anonymous)")
def test_checkout_add_shipping_address_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to shipping mode"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()
        expect(
            cart_page.shipping_details_section.shipping_address_section.select_address_button
        ).to_be_visible()

    with allure.step("Open edit-address modal and submit a new address"):
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        edit_address_modal = EditAddressModal(
            root=page.locator("[data-test-id='edit-address-modal']")
        )
        expect(edit_address_modal.root).to_be_visible()
        edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
        expect(edit_address_modal.submit_button).to_be_enabled()
        edit_address_modal.submit_button.click()

    with allure.step("Verify the submitted address is shown as the current shipping address"):
        expect(edit_address_modal.root).not_to_be_visible()
        expect(
            cart_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()
        expect(
            cart_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_contain_text(str(TEST_CART_ADDRESS.line1))


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Pick a saved shipping address on single-page checkout")
def test_checkout_select_shipping_address_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to shipping mode"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()
        expect(
            cart_page.shipping_details_section.shipping_address_section.select_address_button
        ).to_be_visible()

    with allure.step(f"Open select-address modal and pick the address with '{_ADDRESS_FRAGMENT}'"):
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()
        address = select_address_modal.find_address(text=_ADDRESS_FRAGMENT)
        expect(address).to_be_visible()
        address.click()
        expect(select_address_modal.ok_button).to_be_enabled()
        select_address_modal.ok_button.click()

    with allure.step("Verify selected address is reflected on the shipping section"):
        expect(select_address_modal.root).not_to_be_visible()
        expect(
            cart_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country on single-page checkout")
def test_checkout_filter_shipping_address_by_country_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to shipping mode"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.select_address_button
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}' and verify chip"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country and region on single-page checkout")
def test_checkout_filter_shipping_address_by_region_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to shipping mode"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.select_address_button
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        select_address_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        cart_page.click_outside()
        region_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country, region and city on single-page checkout")
def test_checkout_filter_shipping_address_by_city_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to shipping mode"):
        cart_page.navigate()
        expect(cart_page.shipping_details_section.root).to_be_visible()
        cart_page.shipping_details_section.shipping_switcher.click()
        expect(
            cart_page.shipping_details_section.shipping_address_section.select_address_button
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        cart_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        cart_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        select_address_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        cart_page.click_outside()
        region_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Apply city filter '{_FILTER_CITY}'"):
        select_address_modal.city_filter_selector.select_item_by_name(name=_FILTER_CITY)
        cart_page.click_outside()
        city_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region/city filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Add a new shipping address on multi-step checkout (anonymous)")
def test_checkout_add_shipping_address_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to shipping mode on the shipping checkout page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Open edit-address modal and submit a new address"):
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        edit_address_modal = EditAddressModal(
            root=page.locator("[data-test-id='edit-address-modal']")
        )
        expect(edit_address_modal.root).to_be_visible()
        edit_address_modal.address_form.fill(address=TEST_CART_ADDRESS)
        expect(edit_address_modal.submit_button).to_be_enabled()
        edit_address_modal.submit_button.click()

    with allure.step("Verify the submitted address is reflected on the shipping section"):
        expect(edit_address_modal.root).not_to_be_visible()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_contain_text(str(TEST_CART_ADDRESS.line1))


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Pick a saved shipping address on multi-step checkout")
def test_checkout_select_shipping_address_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to shipping mode on the shipping checkout page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step(f"Open select-address modal and pick the address with '{_ADDRESS_FRAGMENT}'"):
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()
        address = select_address_modal.find_address(text=_ADDRESS_FRAGMENT)
        expect(address).to_be_visible()
        address.click()
        expect(select_address_modal.ok_button).to_be_enabled()
        select_address_modal.ok_button.click()

    with allure.step("Verify selected address is reflected on the shipping section"):
        expect(select_address_modal.root).not_to_be_visible()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.current_address_label
        ).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country on multi-step checkout")
def test_checkout_filter_shipping_address_by_country_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to shipping mode on the shipping checkout page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}' and verify chip"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        shipping_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country and region on multi-step checkout")
def test_checkout_filter_shipping_address_by_region_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to shipping mode on the shipping checkout page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        shipping_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        select_address_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        shipping_page.click_outside()
        region_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Shipping address (E2E)")
@allure.title("Filter saved shipping addresses by country, region and city on multi-step checkout")
def test_checkout_filter_shipping_address_by_city_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        expect(cart_page.checkout_button).to_be_visible()
        expect(cart_page.checkout_button).to_be_enabled()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to shipping mode on the shipping checkout page"):
        expect(shipping_page.shipping_details_section.root).to_be_visible()
        shipping_page.shipping_details_section.shipping_switcher.click()
        expect(
            shipping_page.shipping_details_section.shipping_address_section.root
        ).to_be_visible()

    with allure.step("Open the select-address modal"):
        shipping_page.shipping_details_section.shipping_address_section.select_address_button.click()
        select_address_modal = SelectAddressModal(
            root=page.locator("[data-test-id='select-address-modal']")
        )
        expect(select_address_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_FILTER_COUNTRY}'"):
        select_address_modal.country_filter_selector.select_item_by_name(name=_FILTER_COUNTRY)
        shipping_page.click_outside()
        country_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_FILTER_REGION}'"):
        select_address_modal.region_filter_selector.select_item_by_name(name=_FILTER_REGION)
        shipping_page.click_outside()
        region_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_REGION)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Apply city filter '{_FILTER_CITY}'"):
        select_address_modal.city_filter_selector.select_item_by_name(name=_FILTER_CITY)
        shipping_page.click_outside()
        city_chip = select_address_modal.find_applied_filter_chip_by_name(name=_FILTER_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify the '{_ADDRESS_FRAGMENT}' address matches the country/region/city filter"):
        expect(select_address_modal.addresses.first).to_be_visible()
        expect(select_address_modal.find_address(text=_ADDRESS_FRAGMENT)).to_be_visible()
