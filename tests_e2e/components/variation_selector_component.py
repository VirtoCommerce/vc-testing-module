from playwright.sync_api import Locator

from .variation_option_component import VariationOptionComponent


class VariationSelectorComponent:

    def __init__(self, element: Locator):
        self.element = element

    @property
    def is_visible(self) -> bool:
        """Check if the variation selector is visible on the page."""
        return self.element.locator("[data-test-id^='variant-picker-group--']").first.is_visible()

    @property
    def option_groups(self) -> list[Locator]:
        """Return all variant picker group elements."""
        return self.element.locator("[data-test-id^='variant-picker-group--']").all()

    def get_option_group_by_name(self, name: str) -> Locator | None:
        """Find a variant picker group by property name.

        Matches against the data-test-id property key or the parent wrapper text content.
        """
        groups = self.option_groups
        for group in groups:
            test_id = group.get_attribute("data-test-id") or ""
            property_key = test_id.replace("variant-picker-group--", "")

            parent_wrapper = group.locator("..")
            wrapper_text = parent_wrapper.text_content() or ""

            if name.lower() in wrapper_text.lower() or name.lower().replace(" ", "") == property_key.lower():
                return group
        return None

    def get_options_for_group(self, group_name: str) -> list[VariationOptionComponent]:
        """Return all option components within a named group."""
        group = self.get_option_group_by_name(group_name)
        if not group:
            return []
        buttons = group.locator("[data-test-id^='variant-picker--']").all()
        return [VariationOptionComponent(btn) for btn in buttons]

    def select_option(self, group_name: str, option_value: str) -> bool:
        """Select an option by value within a named group.

        First tries direct data-test-id match, then falls back to aria-label matching.
        """
        group = self.get_option_group_by_name(group_name)
        if not group:
            return False

        test_id = group.get_attribute("data-test-id") or ""
        property_key = test_id.replace("variant-picker-group--", "")

        option_locator = group.locator(f"[data-test-id='variant-picker--{property_key}--{option_value}']")
        if option_locator.count() > 0:
            option_locator.click()
            return True

        options = self.get_options_for_group(group_name)
        for option in options:
            if option.label_text == option_value:
                option.click()
                return True
        return False

    def get_selected_option(self, group_name: str) -> VariationOptionComponent | None:
        """Return the currently selected option in a named group, or None."""
        options = self.get_options_for_group(group_name)
        for option in options:
            if option.is_selected:
                return option
        return None

    def get_available_options(self, group_name: str) -> list[VariationOptionComponent]:
        """Return all enabled options within a named group."""
        options = self.get_options_for_group(group_name)
        return [opt for opt in options if opt.is_available]

    def get_unavailable_options(self, group_name: str) -> list[VariationOptionComponent]:
        """Return all disabled options within a named group."""
        options = self.get_options_for_group(group_name)
        return [opt for opt in options if not opt.is_available]

    def get_available_options_count(self, group_name: str) -> int:
        """Return the count of enabled options within a named group."""
        return len(self.get_available_options(group_name))

    def get_total_options_count(self, group_name: str) -> int:
        """Return the total count of options within a named group."""
        return len(self.get_options_for_group(group_name))

    def get_all_group_names(self) -> list[str]:
        """Return display names for all variant picker groups.

        Reads the label from the first child element of each group's parent wrapper.
        """
        names = []
        for group in self.option_groups:
            parent_wrapper = group.locator("..")
            label_el = parent_wrapper.locator("> *").first
            label_text = label_el.text_content()
            if label_text:
                names.append(label_text.strip())
        return names

    def are_all_groups_selected(self) -> bool:
        """Check if every variant group has a selected option."""
        for group_name in self.get_all_group_names():
            if self.get_selected_option(group_name) is None:
                return False
        return True
