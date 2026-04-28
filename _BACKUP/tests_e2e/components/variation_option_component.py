from playwright.sync_api import Locator


class VariationOptionComponent:

    def __init__(self, element: Locator):
        self.element = element

    @property
    def is_selected(self) -> bool:
        """Check if this option is currently selected (has vc-variant-picker--active class)."""
        class_attr = self.element.evaluate("el => el.closest('.vc-variant-picker')?.className || ''")
        return "vc-variant-picker--active" in str(class_attr)

    @property
    def label_text(self) -> str | None:
        """Get the display text from aria-label."""
        return self.element.get_attribute("aria-label")

    def click(self) -> None:
        """Click to select this option."""
        self.element.click()
