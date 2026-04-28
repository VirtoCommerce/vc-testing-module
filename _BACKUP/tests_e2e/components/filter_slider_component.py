from playwright.sync_api import Locator


class FilterSliderComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def is_expanded(self) -> bool:
        return self.element.locator(".vc-widget__slot-container").is_visible()

    @property
    def lower_handler(self) -> Locator:
        return self.element.locator(".noUi-handle-lower")

    @property
    def upper_handler(self) -> Locator:
        return self.element.locator(".noUi-handle-upper")

    @property
    def lower_input(self) -> Locator:
        return self.element.locator("[data-test-id='slider-input-start']")

    @property
    def upper_input(self) -> Locator:
        return self.element.locator("[data-test-id='slider-input-end']")

    def click_header(self) -> None:
        self.element.locator(".vc-widget__header-container").click()

    def set_lower_value(self, value: int) -> None:
        self.lower_handler.evaluate(f"el => el.setAttribute('aria-valuetext', {value})")

    def set_upper_value(self, value: int) -> None:
        self.upper_handler.evaluate(f"el => el.setAttribute('aria-valuetext', {value})")
