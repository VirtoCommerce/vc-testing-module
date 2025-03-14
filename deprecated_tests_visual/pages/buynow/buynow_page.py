from .buynow_locators import BuynowLocators
from utils.element_mock_text import element_mock_text
from utils.element_replace_numbers_in_text import element_replace_numbers_in_text


class BuynowPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = BuynowLocators()

    def navigate(self):
        """Navigate to buynow page with specific filters"""
        filtered_url = f"{self.config['base_url']}/search/products?facets=%22SupplierOuterId%22:%22autotests-visual-supplier-outer-id%22+%22MarketingTags%22:%22Top40%22"
        self.page.goto(filtered_url)
        self.page.wait_for_url(filtered_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")

    def mock_product_name(self):
        """Mock the product name text"""
        element_mock_text(self.page, self.locators.PRODUCT_NAME, "mocked text")

    def mock_results_count(self):
        """Mock the 'out of' results number"""
        results_out_of = self.page.get_by_text(self.locators.RESULTS_OUT_OF)
        element_replace_numbers_in_text(self.page, results_out_of, replacement="888")
