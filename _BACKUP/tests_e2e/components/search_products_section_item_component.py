from playwright.sync_api import Locator


class SearchProductsSectionItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def product_link(self) -> Locator:
        return self.element.locator(".vc-product-title__text")

    @property
    def name(self) -> str:
        return self.element.locator(".vc-product-title__text").text_content()
