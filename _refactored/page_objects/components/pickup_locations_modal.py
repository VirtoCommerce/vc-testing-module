from playwright.sync_api import Locator

from .chip import Chip
from .component import Component
from .dropdown_filter import DropdownFilter


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

    def find_applied_filter_chip_by_name(self, name: str) -> Chip:
        return Chip(self.applied_filters_chips.filter(has_text=name))
