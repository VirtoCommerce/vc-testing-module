from playwright.sync_api import Locator


class VariationOptionComponent:
    """Component for individual variation option (e.g., a single size or color option)."""

    def __init__(self, element: Locator):
        self.element = element

    @property
    def value(self) -> str | None:
        """Get the option value from data attribute."""
        return self.element.get_attribute("data-option-value")

    @property
    def is_selected(self) -> bool:
        """Check if this option is currently selected."""
        return self.element.get_attribute("data-selected") == "true"

    @property
    def is_available(self) -> bool:
        """Check if this option is available (in stock)."""
        return self.element.get_attribute("data-available") != "false"

    @property
    def is_disabled(self) -> bool:
        """Check if the option element is disabled."""
        return self.element.is_disabled()

    @property
    def label(self) -> Locator:
        """Get the label element for this option."""
        return self.element.locator("[data-test-id='option-label']")

    @property
    def label_text(self) -> str | None:
        """Get the text content of the option label."""
        return self.label.text_content()

    def click(self) -> None:
        """Click to select this option."""
        self.element.click()
