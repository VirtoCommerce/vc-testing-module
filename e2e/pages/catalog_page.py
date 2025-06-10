from playwright.sync_api import Page, expect
import time
from e2e.pages.locators.catalog_locators import CatalogPageLocators
from utils.commonLocators.common_components_locators import CommonComponentsLocators
from playwright.sync_api import BrowserContext


class CatalogPage:
    def __init__(self, page: Page, config: dict = None, browser_context: BrowserContext = None):
        self.page = page
        self.config = config
        self.browser_context = browser_context

    def navigate(self):
        if self.config:
            self.page.goto(self.config["base_url"] + "/catalog")
        else:
            self.page.goto("/catalog")
        self.page.wait_for_load_state("domcontentloaded")

    def scroll_to_bottom(self):
        """Scroll the page to the bottom to load all content"""
        # Get initial page height
        last_height = self.page.evaluate("document.body.scrollHeight")

        # Scroll down in increments
        for _ in range(5):
            # Scroll down
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(2000)  # Wait for content to load

            # Calculate new scroll height
            new_height = self.page.evaluate("document.body.scrollHeight")

            # Break if no more content loaded
            if new_height == last_height:
                break

            last_height = new_height
            print(f"Scrolled to height: {new_height}")

    def add_items_to_cart_one_by_one(self, count):
        """Add items to cart one by one in a loop"""
        print(f"Adding {count} items to cart one by one")
        items_added = 0
        max_scroll_attempts = 5
        scroll_attempts = 0

        try:

            while items_added < count and scroll_attempts < max_scroll_attempts:
                # Find all visible and enabled "Add to cart" buttons
                buttons = self.page.get_by_role("button", name="Add to cart").all()
                print(f"Found {len(buttons)} 'Add to cart' buttons")

                # Filter for visible and enabled buttons
                visible_enabled_buttons = []
                for button in buttons:
                    if button.is_visible() and button.is_enabled():
                        visible_enabled_buttons.append(button)

                print(f"Found {len(visible_enabled_buttons)} visible and enabled 'Add to cart' buttons")

                # If we have buttons, try to click them
                if visible_enabled_buttons:
                    for button in visible_enabled_buttons:
                        if items_added >= count:
                            break

                        try:
                            # Make sure button is visible
                            button.scroll_into_view_if_needed()
                            self.page.wait_for_timeout(500)

                            # Click the button
                            button.click()
                            self.page.wait_for_selector(
                                CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden"
                            )
                            items_added += 1
                            print(f"Added item {items_added}/{count} to cart")

                            # Wait for cart to update
                            self.page.wait_for_timeout(1000)

                        except Exception as e:
                            print(f"Error clicking button: {str(e)}")
                            # Continue with next button

                # If we still need more items, scroll and try again
                if items_added < count:
                    print(f"Need {count - items_added} more items, scrolling to load more products")
                    # Use a more targeted scroll approach instead of full page scroll
                    self.page.evaluate("window.scrollBy(0, 800)")
                    self.page.wait_for_timeout(2000)  # Wait for new products to load
                    scroll_attempts += 1

            # If we still don't have enough items after all scroll attempts, try one more approach
            if items_added < count:
                print("Trying alternative approach with different selector")
                additional_buttons = self.page.locator("button:has-text('Add to cart')").all()

                # Filter for visible and enabled buttons
                visible_enabled_additional = []
                for button in additional_buttons:
                    if button.is_visible() and button.is_enabled():
                        visible_enabled_additional.append(button)

                print(f"Found {len(visible_enabled_additional)} additional visible and enabled buttons")

                # Try to click these buttons
                for button in visible_enabled_additional:
                    if items_added >= count:
                        break

                    try:
                        # Make sure button is visible
                        button.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(500)

                        # Click the button
                        button.click(timeout=5000)
                        items_added += 1
                        print(f"Added item {items_added}/{count} to cart")

                        # Wait for cart to update
                        self.page.wait_for_timeout(1000)

                    except Exception as e:
                        print(f"Error clicking button: {str(e)}")
                        # Continue with next button

        except Exception as e:
            print(f"Unexpected error in add_items_to_cart_one_by_one: {str(e)}")

        print(f"Added {items_added} items to cart")
        return items_added
