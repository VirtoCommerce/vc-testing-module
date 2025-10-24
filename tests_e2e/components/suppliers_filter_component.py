from playwright.sync_api import Locator, Page

class SuppliersFilterComponent:
    def __init__(self, page: Page):
        self.element = page.locator('[opus-test-id="suppliers-filter"]')

    def get_supplier_checkbox(self, supplier_name: str) -> Locator:
        return self.element.locator(
            f'input.vc-checkbox__input[name="{supplier_name}"]'
        )