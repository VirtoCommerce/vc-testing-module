from tests_visual.pages.homepage.homepage_locators import HomepageLocators


class HomePage:
    def __init__(self, page):
        self.page = page

    def wait_for_product_images(self):
        """Wait for all product images to load"""
        images = self.page.locator(HomepageLocators.PRODUCT_IMAGES).all()
        for image in images:
            image_handle = image.element_handle()
            self.page.wait_for_function("element => element.naturalWidth > 0", arg=image_handle, timeout=20000)
