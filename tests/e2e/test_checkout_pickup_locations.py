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
def test_checkout_pickup_locations_country_filter_single_page(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

    pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
    cart_page.click_outside()
    country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
    expect(country_chip.root).to_be_visible()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY)
    assert len(matched) > 0, "No pickup location cards found matching the country filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_pickup_locations_country_region_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

    pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
    cart_page.click_outside()
    country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
    expect(country_chip.root).to_be_visible()

    pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
    cart_page.click_outside()
    region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
    expect(region_chip.root).to_be_visible()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT)
    assert len(matched) > 0, "No pickup location cards found matching the country/region filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_pickup_locations_country_region_city_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
    assert len(matched) > 0, "No pickup location cards found matching the country/region/city filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_pickup_locations_country_region_city_keyword_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.search_keyword_input.fill(_SEARCH_KEYWORD)
    pickup_locations_modal.search_button.click()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
    assert len(matched) > 0, "No pickup location cards found matching the country/region/city/keyword filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_pickup_locations_fake_keyword_returns_no_cards_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(cart_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.search_keyword_input.fill(_FAKE_SEARCH_KEYWORD)
    pickup_locations_modal.search_button.click()

    pickup_locations_modal.wait_for_results()
    expect(pickup_locations_modal.pickup_location_cards).to_have_count(0)


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_pickup_locations_country_filter_multi_step(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

    pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
    shipping_page.click_outside()
    country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
    expect(country_chip.root).to_be_visible()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY)
    assert len(matched) > 0, "No pickup location cards found matching the country filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_pickup_locations_country_region_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

    pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
    shipping_page.click_outside()
    country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_COUNTRY)
    expect(country_chip.root).to_be_visible()

    pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION_FULL)
    shipping_page.click_outside()
    region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION_FULL)
    expect(region_chip.root).to_be_visible()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT)
    assert len(matched) > 0, "No pickup location cards found matching the country/region filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_pickup_locations_country_region_city_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
    assert len(matched) > 0, "No pickup location cards found matching the country/region/city filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_pickup_locations_country_region_city_keyword_filter_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.search_keyword_input.fill(_SEARCH_KEYWORD)
    pickup_locations_modal.search_button.click()

    pickup_locations_modal.wait_for_results()
    matched = pickup_locations_modal.find_pickup_location_cards(country=_COUNTRY, region=_REGION_SHORT, city=_CITY)
    assert len(matched) > 0, "No pickup location cards found matching the country/region/city/keyword filter"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_pickup_locations_fake_keyword_returns_no_cards_multi_step(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    shipping_page.shipping_details_section.pickup_switcher.click()
    expect(shipping_page.shipping_details_section.pickup_location_section.root).to_be_visible()

    shipping_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(root=page.locator("[data-test-id='pickup-locations-modal']"))
    expect(pickup_locations_modal.root).to_be_visible()

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

    pickup_locations_modal.search_keyword_input.fill(_FAKE_SEARCH_KEYWORD)
    pickup_locations_modal.search_button.click()

    pickup_locations_modal.wait_for_results()
    expect(pickup_locations_modal.pickup_location_cards).to_have_count(0)
