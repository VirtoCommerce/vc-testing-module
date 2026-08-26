from typing import Final

from playwright.sync_api import Locator, expect

from page_objects.backend.page_builder.constants import (
    DetailsToolbar,
    Field,
    Section,
)
from page_objects.backend.shell import (
    Blade,
    Card,
    ConfirmationPopup,
    DatePicker,
    Select,
)

_PERMALINK_PREFIX: Final = "div[class*='tw-rounded-sm']"
_DATE_INPUT: Final = "[data-test-id='dp-input']"
_SWITCH: Final = ".vc-switch"
_SWITCH_INPUT: Final = "input[role='switch']"


class PageDetailsBlade(Blade):
    @property
    def basic_section(self) -> Card:
        return self.card(Section.BASIC)

    @property
    def personalization_section(self) -> Card:
        return self.card(Section.PERSONALIZATION)

    @property
    def scheduling_section(self) -> Card:
        return self.card(Section.SCHEDULING)

    @property
    def name_input(self) -> Locator:
        return self.text_input(Field.NAME)

    @property
    def permalink_input(self) -> Locator:
        return self.text_input(Field.PERMALINK)

    @property
    def permalink_prefix(self) -> Locator:
        return self.field(Field.PERMALINK).locator(_PERMALINK_PREFIX).first

    @property
    def language(self) -> Select:
        return self.select(Field.LANGUAGE)

    @property
    def user_groups(self) -> Select:
        return self.select(Field.USER_GROUPS)

    @property
    def organization(self) -> Select:
        return self.select(Field.ORGANIZATION)

    @property
    def visibility_label(self) -> Locator:
        return self.label(Field.VISIBILITY)

    @property
    def visibility_toggle(self) -> Locator:
        return self._root.locator(_SWITCH_INPUT).first

    @property
    def visibility_control(self) -> Locator:
        return self._root.locator(_SWITCH).first

    @property
    def is_visible_to_all(self) -> bool:
        return self.visibility_toggle.is_checked()

    def set_visibility(self, enabled: bool) -> None:
        if self.is_visible_to_all != enabled:
            self.visibility_control.click()

    def date_picker(self, label: str) -> DatePicker:
        return DatePicker(self.field(label))

    def date_input(self, label: str) -> Locator:
        return self.field(label).locator(_DATE_INPUT).first

    @property
    def start_date(self) -> DatePicker:
        return self.date_picker(Field.START_DATE)

    @property
    def end_date(self) -> DatePicker:
        return self.date_picker(Field.END_DATE)

    @property
    def start_date_input(self) -> Locator:
        return self.date_input(Field.START_DATE)

    @property
    def end_date_input(self) -> Locator:
        return self.date_input(Field.END_DATE)

    def wait_until_ready(self) -> "PageDetailsBlade":
        self.name_input.wait_for(state="visible")
        return self

    def wait_until_loaded(self) -> "PageDetailsBlade":
        self.wait_until_ready()
        expect(self.name_input).not_to_have_value("")
        return self

    def fill(self, *, name: str | None = None, permalink: str | None = None) -> None:
        if name is not None:
            self.name_input.fill(name)
        if permalink is not None:
            self.permalink_input.fill(permalink)

    @property
    def can_save(self) -> bool:
        return self.toolbar.is_enabled(DetailsToolbar.SAVE)

    def save(self) -> None:
        self.toolbar.click(DetailsToolbar.SAVE)

    def publish(self) -> None:
        self.toolbar.click(DetailsToolbar.PUBLISH)

    def unpublish(self) -> None:
        self.toolbar.click(DetailsToolbar.UNPUBLISH)

    def clone(self) -> None:
        self.toolbar.click(DetailsToolbar.CLONE)

    def open_designer(self) -> Locator:
        return self.toolbar.button(DetailsToolbar.OPEN_DESIGNER)

    def wait_settled(self) -> None:
        self._root.page.wait_for_load_state("networkidle")

    def archive(self, confirm: bool = True) -> None:
        self.toolbar.click(DetailsToolbar.ARCHIVE)
        popup = ConfirmationPopup.on(self._root.page)
        if not confirm:
            popup.cancel()
            return
        popup.confirm()
        self.wait_settled()
