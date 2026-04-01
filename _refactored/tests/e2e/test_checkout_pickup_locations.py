import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.components import PickupLocationsModal
from page_objects.pages import CartPage

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3
_COUNTRY = "United States of America"
_REGION = "District of Columbia"
_CITY = "Washington"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_pickup_locations_country_region_city_filter_single_page(
    global_settings: GlobalSettings, page: Page
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    cart_page.shipping_details_section.pickup_switcher.click()
    expect(
        cart_page.shipping_details_section.pickup_location_section.root
    ).to_be_visible()

    cart_page.shipping_details_section.pickup_location_section.select_address_button.click()

    pickup_locations_modal = PickupLocationsModal(
        root=page.locator("[data-test-id='pickup-locations-modal']")
    )
    expect(pickup_locations_modal.root).to_be_visible()

    pickup_locations_modal.country_filter_selector.select_item_by_name(name=_COUNTRY)
    cart_page.click_outside()
    country_chip = pickup_locations_modal.find_applied_filter_chip_by_name(
        name=_COUNTRY
    )
    expect(country_chip.root).to_be_visible()

    pickup_locations_modal.region_filter_selector.select_item_by_name(name=_REGION)
    cart_page.click_outside()
    region_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_REGION)
    expect(region_chip.root).to_be_visible()

    pickup_locations_modal.city_filter_selector.select_item_by_name(name=_CITY)
    cart_page.click_outside()
    city_chip = pickup_locations_modal.find_applied_filter_chip_by_name(name=_CITY)
    expect(city_chip.root).to_be_visible()
