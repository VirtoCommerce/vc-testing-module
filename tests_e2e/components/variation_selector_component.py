from playwright.sync_api import Locator

from .variation_option_component import VariationOptionComponent


class VariationSelectorComponent:
    """Component for B2C product variation selector (SKU selector with option groups)."""

    def __init__(self, element: Locator):
        self.element = element

    @property
    def is_visible(self) -> bool:
        """Check if the variation selector is visible."""
        return self.element.is_visible()

    @property
    def option_groups(self) -> list[Locator]:
        """Get all option group containers (e.g., Color group, Size group)."""
        return self.element.locator("[data-test-id='variation-option-group']").all()

    @property
    def validation_message(self) -> Locator:
        """Get the validation message element (shown when selection is incomplete)."""
        return self.element.locator("[data-test-id='variation-selector.validation-message']")

    @property
    def validation_message_text(self) -> str | None:
        """Get the text content of the validation message."""
        if self.validation_message.is_visible():
            return self.validation_message.text_content()
        return None

    def get_option_group_by_name(self, name: str) -> Locator | None:
        """Find an option group by its label name (e.g., 'Color', 'Size')."""
        for group in self.option_groups:
            label = group.locator("[data-test-id='option-group-label']").text_content()
            if label and name.lower() in label.lower():
                return group
        return None

    def get_options_for_group(self, group_name: str) -> list[VariationOptionComponent]:
        """Get all options within a specific group."""
        group = self.get_option_group_by_name(group_name)
        if not group:
            return []
        return [VariationOptionComponent(option) for option in group.locator("[data-test-id='variation-option']").all()]

    def select_option(self, group_name: str, option_value: str) -> bool:
        """Select an option by group name and option value. Returns True if found and clicked."""
        options = self.get_options_for_group(group_name)
        for option in options:
            if option.value == option_value or option.label_text == option_value:
                option.click()
                return True
        return False

    def get_selected_option(self, group_name: str) -> VariationOptionComponent | None:
        """Get the currently selected option in a group."""
        options = self.get_options_for_group(group_name)
        for option in options:
            if option.is_selected:
                return option
        return None

    def get_available_options(self, group_name: str) -> list[VariationOptionComponent]:
        """Get all available (in-stock) options in a group."""
        options = self.get_options_for_group(group_name)
        return [opt for opt in options if opt.is_available]

    def get_unavailable_options(self, group_name: str) -> list[VariationOptionComponent]:
        """Get all unavailable (out-of-stock) options in a group."""
        options = self.get_options_for_group(group_name)
        return [opt for opt in options if not opt.is_available]

    def get_available_options_count(self, group_name: str) -> int:
        """Count available options in a group."""
        return len(self.get_available_options(group_name))

    def get_total_options_count(self, group_name: str) -> int:
        """Count total options in a group."""
        return len(self.get_options_for_group(group_name))

    def get_all_group_names(self) -> list[str]:
        """Get names of all option groups."""
        names = []
        for group in self.option_groups:
            label = group.locator("[data-test-id='option-group-label']").text_content()
            if label:
                names.append(label.strip())
        return names

    def are_all_groups_selected(self) -> bool:
        """Check if all option groups have a selection made."""
        for group_name in self.get_all_group_names():
            if self.get_selected_option(group_name) is None:
                return False
        return True
