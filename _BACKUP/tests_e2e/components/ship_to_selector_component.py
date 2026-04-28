from playwright.sync_api import Locator


class ShipToSelectorComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def trigger_button(self) -> Locator:
        
        return self.element.locator(".ship-to-selector__trigger")

    @property
    def select_address_label(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-label']")

    @property
    def selected_address_label(self) -> Locator:
        return self.element.locator("[data-test-id='selected-address-label']")

    @property
    def shipping_addresses_dropdown(self) -> Locator:
        return self.element.locator("[data-test-id='shipping-addresses-list']")

    @property
    def shipping_addresses(self) -> list[Locator]:
        return self.element.locator("button.ship-to-selector__item").all()

    @property
    def add_new_address_button(self) -> Locator:
        return self.element.locator("[data-test-id='ship-to-add-new-address']")

    @property
    def search_field(self) -> Locator:
        return self.element.locator("[data-test-id='ship-to-search-field']")

    @property
    def more_button(self) -> Locator:
        return self.element.locator("[data-test-id='ship-to-more-button']")

    def favorite_icon(self, address_id: str) -> Locator:
        return self.element.locator(f"[data-test-id='ship-to-favorite-icon-{address_id}']")