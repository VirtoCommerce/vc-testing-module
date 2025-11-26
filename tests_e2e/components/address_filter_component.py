from playwright.sync_api import Locator

from tests_e2e.components.facet_component import FacetComponent


class AddressFilterComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def filter_countries(self) -> FacetComponent:
        return FacetComponent(self.element.locator("[data-test-id='select-address-filter-countries']"))

    @property
    def filter_regions(self) -> FacetComponent:
        return FacetComponent(self.element.locator("[data-test-id='select-address-filter-regions']"))

    @property
    def filter_cities(self) -> FacetComponent:
        return FacetComponent(self.element.locator("[data-test-id='select-address-filter-cities']"))

    @property
    def filter_keyword_input(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-filter-keyword-input']")

    @property
    def apply_button(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-filter-apply-button']")
