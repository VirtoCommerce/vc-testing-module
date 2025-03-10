from .order_review_locators import OrderReviewLocators


class OrderReviewPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = OrderReviewLocators()
