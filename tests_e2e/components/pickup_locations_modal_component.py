from playwright.sync_api import Locator, Page

from .pickup_location_card_dialog_component import PickupLocationCardDialogComponent


class PickupLocationsModalComponent:
    """Component for the product page pickup locations modal dialog.

    This modal is opened via the "Check pickup locations" button on the product page.
    It contains a search box, a list of pickup locations, and a Google Map.
    """

    def __init__(self, element: Locator, page: Page):
        self.element = element
        self.page = page

    @property
    def search_keyword_input(self) -> Locator:
        return self.element.locator("[data-test-id='search-keyword-input']")

    @property
    def search_button(self) -> Locator:
        return self.element.locator("[data-test-id='search-button']")

    @property
    def pickup_locations_list(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-locations-list']")

    @property
    def pickup_location_items(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-item']")

    @property
    def pickup_location_names(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-name']")

    @property
    def pickup_location_addresses(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-address']")

    @property
    def pickup_availability_chips(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-availability-chip']")

    @property
    def pickup_locations_map(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-locations-map']")

    @property
    def select_address_map_desktop(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-map-desktop']")

    @property
    def pickup_locations_not_found(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-locations-not-found']")

    @property
    def reset_search_button(self) -> Locator:
        return self.element.locator("[data-test-id='reset-search-button']")

    @property
    def close_button(self) -> Locator:
        return self.element.locator("button[aria-label='Close']")

    @property
    def pickup_location_card(self) -> PickupLocationCardDialogComponent:

        return PickupLocationCardDialogComponent(self.page.locator("[data-test-id='pickup-location-card']"))

    def get_location_item_by_index(self, index: int) -> Locator:
        """Get a specific pickup location list item by its zero-based index."""
        return self.pickup_location_items.nth(index)

    def get_location_name_by_index(self, index: int) -> Locator:
        """Get the name element of a specific pickup location by its zero-based index."""
        return self.pickup_location_names.nth(index)

    def get_location_address_by_index(self, index: int) -> Locator:
        """Get the address element of a specific pickup location by its zero-based index."""
        return self.pickup_location_addresses.nth(index)

    def get_availability_chip_by_index(self, index: int) -> Locator:
        """Get the availability chip of a specific pickup location by its zero-based index."""
        return self.pickup_availability_chips.nth(index)

    def search(self, keyword: str) -> None:
        self.search_keyword_input.fill(keyword)
        self.search_keyword_input.press("Enter")

    def wait_for_search_results(self, timeout: int = 10_000) -> None:

        first_item = self.pickup_location_items.first
        not_found = self.pickup_locations_not_found

        # Use Playwright's built-in `or_` combinator to wait for either state.
        first_item.or_(not_found).wait_for(state="visible", timeout=timeout)

    def click_location_by_index(self, index: int) -> None:

        self.pickup_location_items.nth(index).locator(".vc-radio-button").click()

    def clear_search(self) -> None:
        self.search_keyword_input.clear()
        self.search_keyword_input.press("Enter")

    def wait_for_map_ready(self, timeout: int = 15_000) -> None:

        self.pickup_locations_map.wait_for(state="visible", timeout=timeout)
        markers = self.pickup_locations_map.locator("gmp-advanced-marker")
        if markers.count() > 0:
            markers.first.wait_for(state="attached", timeout=timeout)
        else:
            self.pickup_locations_map.locator("button[aria-label]").first.wait_for(state="attached", timeout=timeout)
