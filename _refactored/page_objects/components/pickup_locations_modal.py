from playwright.sync_api import Locator

from .chip import Chip
from .component import Component
from .dropdown_filter import DropdownFilter
from .pickup_location_card import PickupLocationCard


class PickupLocationsModal(Component):
    @property
    def country_filter_selector(self) -> DropdownFilter:
        return DropdownFilter(self._root.locator("[data-test-id='filter-country']"))

    @property
    def region_filter_selector(self) -> DropdownFilter:
        return DropdownFilter(self._root.locator("[data-test-id='filter-region']"))

    @property
    def city_filter_selector(self) -> DropdownFilter:
        return DropdownFilter(self._root.locator("[data-test-id='filter-city']"))

    @property
    def applied_filters_chips(self) -> Locator:
        return self._root.locator(".vc-chip")

    @property
    def search_keyword_input(self) -> Locator:
        return self._root.locator("[data-test-id='search-keyword-input']")

    @property
    def search_button(self) -> Locator:
        return self._root.locator("[data-test-id='search-button']")

    @property
    def pickup_location_cards(self) -> Locator:
        return self._root.locator(".select-address-map-list__item")

    def find_pickup_location_cards(
        self,
        country: str | None = None,
        region: str | None = None,
        city: str | None = None,
        name: str | None = None,
    ) -> list[PickupLocationCard]:
        items = [PickupLocationCard(root=loc) for loc in self.pickup_location_cards.all()]
        if country is not None:
            items = [c for c in items if c.country == country]
        if region is not None:
            items = [c for c in items if c.region == region]
        if city is not None:
            items = [c for c in items if c.city == city]
        if name is not None:
            items = [c for c in items if c.name == name]
        return items

    def find_applied_filter_chip_by_name(self, name: str) -> Chip:
        return Chip(self.applied_filters_chips.filter(has_text=name))
