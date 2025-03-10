from PIL import Image
from io import BytesIO
from tests_visual.pages.billing.billing_page import BillingPage
from tests_visual.pages.shipping.shipping_page import ShippingPage
from tests_visual.pages.header.header_page import HeaderPage
from tests_visual.pages.cart.cart_page import CartPage
from utils.add_product_to_cart_util import add_test_product_to_cart


def test_visual_billing(
    authenticated_page,
    config,
    image_snapshot,
    graphql_client,
    user_context,
    clear_cart_if_not_empty,
) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    shipping = ShippingPage(page, config)
    billing = BillingPage(page, config)
    cart = CartPage(page, config)

    # Add product using common utility
    add_test_product_to_cart(graphql_client, user_context)

    # Navigate through cart to shipping
    cart.navigate()
    cart.proceed_to_shipping()

    # Select delivery and proceed to billing
    shipping.select_delivery_method()
    shipping.proceed_to_billing()

    # Complete billing steps
    billing.select_payment_method()
    header.hide_vc_badge()

    # Take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/billing/billing_snapshots/billing_base.png", True)
