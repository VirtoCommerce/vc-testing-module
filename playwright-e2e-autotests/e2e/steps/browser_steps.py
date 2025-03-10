import allure
from playwright.sync_api import expect


class BrowserSteps:
    def __init__(self, page):
        self.page = page

    @allure.step("Open cart with browser")
    def open_cart(self):
        self.page.open()

    @allure.step("Check product is in cart")
    def check_product_is_in_cart(self, product_name):
        expect(self.page.product_list).to_contain_text(product_name)

    @allure.step("Clear cart")
    def clear_cart(self):
        self.page.button_clear_cart.click()
        self.page.button_popup_delete.click()

        expect(self.page.cart_is_empty_heading).to_be_visible()
