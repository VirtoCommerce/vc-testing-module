from .product_locators import ProductLocators
from utils.element_mock_text import element_mock_text
from utils.element_replace_numbers_in_text import element_replace_numbers_in_text
from tests_visual.test_data.test_product import TEST_PRODUCT_2 as product_data

class ProductPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = ProductLocators()
    
    def navigate(self):
        """Navigate to category page with specific filters"""
        filtered_url = f"{self.config['base_url']}{product_data['slug']}"
        self.page.goto(filtered_url)
        self.page.wait_for_url(filtered_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")

    def click_see_more_button(self):
        button = self.page.get_by_role("button", name=self.locators.SEE_MORE_BUTTON).all()[0].click()
        
    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")
