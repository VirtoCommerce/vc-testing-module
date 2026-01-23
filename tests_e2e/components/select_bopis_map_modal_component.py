from playwright.sync_api import Locator

from tests_e2e.components import (
    ChipComponent,
    FilterDropdownComponent,
    PickupLocationListItemComponent,
)


class SelectBopisMapModalComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def pickup_locations_list(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-locations-list']")

    @property
    def pickup_locations(self) -> list[PickupLocationListItemComponent]:
        self.element.wait_for(state="attached", timeout=10_000)
        self.element.wait_for(state="visible", timeout=10_000)
        locations = self.pickup_locations_list.locator(
            "[data-address-id^='pickup-location-']"
        ).all()
        return [PickupLocationListItemComponent(loc) for loc in locations]

    @property
    def filter_countries_dropdown(self) -> FilterDropdownComponent:
        return FilterDropdownComponent(
            self.element.locator("[data-test-id='filter-country']")
        )

    @property
    def filter_regions_dropdown(self) -> FilterDropdownComponent:
        return FilterDropdownComponent(
            self.element.locator("[data-test-id='filter-region']")
        )

    @property
    def filter_cities_dropdown(self) -> FilterDropdownComponent:
        return FilterDropdownComponent(
            self.element.locator("[data-test-id='filter-city']")
        )

    @property
    def search_pickup_location_input(self) -> Locator:
        return self.element.locator("[data-test-id='search-keyword-input']")

    @property
    def search_button(self) -> Locator:
        return self.element.locator("[data-test-id='search-button']")

    @property
    def applied_filters_panel(self) -> Locator:
        return self.element.locator(".select-address-filter__applied-filter")

    @property
    def applied_filters_chips(self) -> list[ChipComponent]:
        return [
            ChipComponent(chip)
            for chip in self.applied_filters_panel.locator(".vc-chip").all()
        ]

    @property
    def reset_filters_chip(self) -> Locator:
        return self.element.locator("[data-test-id='reset-filters-chip']")

    @property
    def map_element(self) -> Locator:
        return self.element.locator(".select-address-map-modal__map")

    @property
    def map_markers(self) -> list[Locator]:
        return self.map_element.locator(":scope >> gmp-advanced-marker").all()

    @property
    def save_button(self) -> Locator:
        return self.element.locator("[data-test-id='save-button']")

    @property
    def cancel_button(self) -> Locator:
        return self.element.locator("[data-test-id='cancel-button']")

    def get_map_marker_by_location_name(self, location_name: str) -> Locator:
        return next(
            marker
            for marker in self.map_markers
            if marker.get_attribute("title") == location_name
        )

    def get_map_marker_by_location_coords(self, coords: str) -> Locator:
        return next(
            marker
            for marker in self.map_markers
            if marker.get_attribute("position") == coords
        )

    def get_applied_filter_chip_by_name(self, name: str) -> ChipComponent:
        return next(chip for chip in self.applied_filters_chips if chip.label == name)

    def get_location_by_name(
        self, location_name: str
    ) -> PickupLocationListItemComponent:
        return next(
            pickup_point
            for pickup_point in self.pickup_locations
            if pickup_point.name == location_name
        )

    def has_pickup_location_with_keyword(self, keyword: str) -> bool:
        return any(
            (keyword in pickup_point.name)
            or (keyword in pickup_point.city)
            or (keyword in pickup_point.region)
            or (keyword in pickup_point.country)
            or (keyword in pickup_point.line1)
            or (keyword in pickup_point.line2)
            for pickup_point in self.pickup_locations
        )
