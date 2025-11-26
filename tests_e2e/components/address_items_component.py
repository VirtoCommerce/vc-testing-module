from playwright.sync_api import Locator

from tests_e2e.components.facet_component import FacetComponent


class AddressItemsComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def radio_buttons(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-map-modal-radio-button']")
