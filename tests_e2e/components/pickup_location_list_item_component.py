from playwright.sync_api import Locator


class PickupLocationListItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def country(self) -> str:
        return self.element.get_attribute("data-country")

    @property
    def region(self) -> str:
        return self.element.get_attribute("data-region")

    @property
    def city(self) -> str:
        return self.element.get_attribute("data-city")

    @property
    def line1(self) -> str:
        return self.element.get_attribute("data-line1")

    @property
    def line2(self) -> str:
        return self.element.get_attribute("data-line2")

    @property
    def name(self) -> str:
        return self.element.get_attribute("data-pickup-point-name")

    @property
    def coords(self) -> str:
        return self.element.get_attribute("data-coords")

    @property
    def is_selected(self) -> bool:
        return self.element.locator(".vc-radio-button__input").is_checked()
