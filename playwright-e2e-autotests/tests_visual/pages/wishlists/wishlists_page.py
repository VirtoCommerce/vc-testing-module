class WishlistsPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config

    def navigate(self):
        """Navigate to wishlists page"""
        self.page.goto(f"{self.config['base_url']}/account/lists")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
