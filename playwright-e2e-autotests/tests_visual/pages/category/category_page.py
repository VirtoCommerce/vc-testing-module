from .category_locators import CategoryLocators
from utils.element_mock_text import element_mock_text
from utils.element_replace_numbers_in_text import element_replace_numbers_in_text


class CategoryPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = CategoryLocators()

    def navigate(self):
        """Navigate to category page with specific filters"""
        filtered_url = f"{self.config['base_url']}/business-products-services?facets=%22SupplierOuterId%22:%22autotests-visual-supplier-outer-id%22+%22MarketingTags%22:%22Top40_Public%22"
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

    def wait_for_product_images(self):
        """Wait for product images to load"""
        images = self.page.locator(self.locators.PRODUCT_IMAGES).all()

        # Scroll down to force lazy loading
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for first 5 images to load
        for image in images[:5]:
            image_handle = image.element_handle()
            self.page.wait_for_function("element => element.naturalWidth > 0", arg=image_handle, timeout=80000)

        # Scroll back to top
        self.page.evaluate("window.scrollTo(0, 0)")
