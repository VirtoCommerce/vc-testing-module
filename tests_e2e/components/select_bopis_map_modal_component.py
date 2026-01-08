from playwright.sync_api import Locator

from tests_e2e.components.pickup_location_list_item_component import (
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
        return [
            PickupLocationListItemComponent(location)
            for location in self.pickup_locations_list.locator(
                "[data-address-id^='pickup-location-']"
            ).all()
        ]

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

    def get_location_by_name(
        self, location_name: str
    ) -> PickupLocationListItemComponent:
        return next(
            location
            for location in self.pickup_locations
            if location.name == location_name
        )

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
