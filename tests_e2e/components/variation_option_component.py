from playwright.sync_api import Locator


class VariationOptionComponent:

    def __init__(self, element: Locator):
        self.element = element

    @property
    def value(self) -> str | None:
        """Get the option value from the data-test-id attribute."""
        test_id = self.element.get_attribute("data-test-id") or ""
        parts = test_id.split("--", 2)
        return parts[2] if len(parts) > 2 else None

    @property
    def is_selected(self) -> bool:
        """Check if this option is currently selected (has vc-variant-picker--active class)."""
        class_attr = self.element.evaluate("el => el.closest('.vc-variant-picker')?.className || ''")
        return "vc-variant-picker--active" in str(class_attr)

    @property
    def is_available(self) -> bool:
        """Check if this option is available (not disabled)."""
        return self.element.is_enabled()

    @property
    def is_disabled(self) -> bool:
        """Check if the option element is disabled."""
        return self.element.is_disabled()

    @property
    def label_text(self) -> str | None:
        """Get the display text from aria-label."""
        return self.element.get_attribute("aria-label")

    def click(self) -> None:
        """Click to select this option."""
        self.element.click()
