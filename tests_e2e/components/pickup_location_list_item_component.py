from playwright.sync_api import Locator


class PickupLocationListItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def name(self) -> str:
        return self.element.locator(
            ".select-address-map-modal__radio-button-name"
        ).text_content()

    @property
    def coords(self) -> str:
        return self.element.locator(
            ".select-address-map-modal__radio-button"
        ).get_attribute("data-test-coords")

    @property
    def is_selected(self) -> bool:
        return self.element.locator(".vc-radio-button__input").is_checked()
