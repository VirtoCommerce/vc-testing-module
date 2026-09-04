from playwright.sync_api import Locator


class Component:
    def __init__(self, root: Locator) -> None:
        self._root = root

    @property
    def root(self) -> Locator:
        return self._root
