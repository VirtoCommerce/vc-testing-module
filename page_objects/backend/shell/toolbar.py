import re
from typing import Final

from playwright.sync_api import Locator, expect

from page_objects.component import Component

DISABLED_CLASS: Final = "vc-blade-toolbar-base-button--disabled"
_DISABLED_PATTERN: Final = re.compile(rf"(^|\s){re.escape(DISABLED_CLASS)}(\s|$)")


class BladeToolbar(Component):
    def button(self, item_id: str) -> Locator:
        return self._root.locator(f"[data-test-id='{item_id}']")

    def click(self, item_id: str) -> None:
        self.button(item_id).click()

    def is_disabled(self, item_id: str) -> bool:
        classes = self.button(item_id).get_attribute("class") or ""
        return DISABLED_CLASS in classes.split()

    def is_enabled(self, item_id: str) -> bool:
        return not self.is_disabled(item_id)

    def expect_disabled(self, item_id: str) -> None:
        expect(self.button(item_id)).to_have_class(_DISABLED_PATTERN)

    def expect_enabled(self, item_id: str) -> None:
        expect(self.button(item_id)).not_to_have_class(_DISABLED_PATTERN)

    @property
    def item_ids(self) -> list[str]:
        return self._root.locator("button[data-test-id]").evaluate_all(
            "nodes => nodes.map(n => n.getAttribute('data-test-id'))"
        )
