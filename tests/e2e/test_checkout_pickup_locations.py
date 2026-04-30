import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import PickupLocationsModal
from page_objects.pages import CartPage, CheckoutShippingPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3
_COUNTRY = "United States of America"
_REGION_FULL = "District of Columbia"
_REGION_SHORT = "DC"
_CITY = "Washington"
_SEARCH_KEYWORD = "TransEuro"
_FAKE_SEARCH_KEYWORD = "NonExistentLocation12345"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country on single-page checkout")
def test_checkout_pickup_locations_country_filter_single_page(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to pickup mode"):
        cart_page.navigate()
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_COUNTRY}' and verify chip"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        cart_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches country '{_COUNTRY}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY)
        assert len(matched) > 0, "No pickup location cards found matching the country filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country and region on single-page checkout")
def test_checkout_pickup_locations_country_region_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to pickup mode"):
        cart_page.navigate()
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_COUNTRY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        cart_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_REGION_FULL}'"):
        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        cart_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches country '{_COUNTRY}' / region '{_REGION_SHORT}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT)
        assert len(matched) > 0, "No pickup location cards found matching the country/region filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country, region and city on single-page checkout")
def test_checkout_pickup_locations_country_region_city_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to pickup mode"):
        cart_page.navigate()
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_COUNTRY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        cart_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Apply region filter '{_REGION_FULL}'"):
        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        cart_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Apply city filter '{_CITY}'"):
        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        cart_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches '{_COUNTRY}' / '{_REGION_SHORT}' / '{_CITY}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
        assert len(matched) > 0, "No pickup location cards found matching the country/region/city filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country/region/city + keyword on single-page checkout")
def test_checkout_pickup_locations_country_region_city_keyword_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to pickup mode"):
        cart_page.navigate()
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region/city filters '{_COUNTRY}' / '{_REGION_FULL}' / '{_CITY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        cart_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        cart_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        cart_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Search by keyword '{_SEARCH_KEYWORD}' and verify cards"):
        pickup_locations_modal.search_keyword_input.fill(_SEARCH_KEYWORD)
        pickup_locations_modal.search_button.click()
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
        assert len(matched) > 0, "No pickup location cards found matching the country/region/city/keyword filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Fake keyword search returns no pickup locations on single-page checkout")
def test_checkout_pickup_locations_fake_keyword_returns_no_cards_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and switch to pickup mode"):
        cart_page.navigate()
        cart_page.shipping_details_section.pickup_switcher.click()
        expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region/city filters '{_COUNTRY}' / '{_REGION_FULL}' / '{_CITY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        cart_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        cart_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        cart_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Search by fake keyword '{_FAKE_SEARCH_KEYWORD}' and verify zero cards"):
        pickup_locations_modal.search_keyword_input.fill(_FAKE_SEARCH_KEYWORD)
        pickup_locations_modal.search_button.click()
        expect(pickup_locations_modal.pickup_location_cards).to_have_count(0)


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country on multi-step checkout")
def test_checkout_pickup_locations_country_filter_multi_step(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to pickup mode on the shipping page"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country filter '{_COUNTRY}' and verify chip"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        shipping_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches country '{_COUNTRY}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY)
        assert len(matched) > 0, "No pickup location cards found matching the country filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country and region on multi-step checkout")
def test_checkout_pickup_locations_country_region_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to pickup mode on the shipping page"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region filters '{_COUNTRY}' / '{_REGION_FULL}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        shipping_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        shipping_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches country '{_COUNTRY}' / region '{_REGION_SHORT}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT)
        assert len(matched) > 0, "No pickup location cards found matching the country/region filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country, region and city on multi-step checkout")
def test_checkout_pickup_locations_country_region_city_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to pickup mode on the shipping page"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region/city filters '{_COUNTRY}' / '{_REGION_FULL}' / '{_CITY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        shipping_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        shipping_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        shipping_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Verify at least one pickup location matches '{_COUNTRY}' / '{_REGION_SHORT}' / '{_CITY}'"):
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
        assert len(matched) > 0, "No pickup location cards found matching the country/region/city filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Filter pickup locations by country/region/city + keyword on multi-step checkout")
def test_checkout_pickup_locations_country_region_city_keyword_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to pickup mode on the shipping page"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region/city filters '{_COUNTRY}' / '{_REGION_FULL}' / '{_CITY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        shipping_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        shipping_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        shipping_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Search by keyword '{_SEARCH_KEYWORD}' and verify cards"):
        pickup_locations_modal.search_keyword_input.fill(_SEARCH_KEYWORD)
        pickup_locations_modal.search_button.click()
        expect(pickup_locations_modal.pickup_location_cards.first).to_be_visible()
        matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
        assert len(matched) > 0, "No pickup location cards found matching the country/region/city/keyword filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
@allure.feature("Checkout / Pickup locations (E2E)")
@allure.title("Fake keyword search returns no pickup locations on multi-step checkout")
def test_checkout_pickup_locations_fake_keyword_returns_no_cards_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page and start checkout"):
        cart_page.navigate()
        cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    with allure.step("Switch to pickup mode on the shipping page"):
        shipping_page.shipping_details_section.pickup_switcher.click()
        expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()
        shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    with allure.step("Verify pickup locations modal is shown"):
        expect(pickup_locations_modal.root).to_be_visible()

    with allure.step(f"Apply country/region/city filters '{_COUNTRY}' / '{_REGION_FULL}' / '{_CITY}'"):
        pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
        shipping_page.click_outside()
        country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
        expect(country_chip.root).to_be_visible()

        pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
        shipping_page.click_outside()
        region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
        expect(region_chip.root).to_be_visible()

        pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
        shipping_page.click_outside()
        city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
        expect(city_chip.root).to_be_visible()

    with allure.step(f"Search by fake keyword '{_FAKE_SEARCH_KEYWORD}' and verify zero cards"):
        pickup_locations_modal.search_keyword_input.fill(_FAKE_SEARCH_KEYWORD)
        pickup_locations_modal.search_button.click()
        expect(pickup_locations_modal.pickup_location_cards).to_have_count(0)
