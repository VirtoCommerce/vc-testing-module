from playwright.sync_api import Locator


class PickupLocationCardDialogComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def name(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-card-name']")

    @property
    def info(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-card-info']")

    @property
    def cancel_button(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-card-cancel']")

    @property
    def select_button(self) -> Locator:
        return self.element.locator("[data-test-id='pickup-location-card-select']")

    @property
    def close_button(self) -> Locator:
        return self.element.locator("button[aria-label='Close']")
