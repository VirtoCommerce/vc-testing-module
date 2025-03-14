from PIL import Image
from io import BytesIO
from tests_visual.pages.cart.cart_page import CartPage
from tests_visual.pages.header.header_page import HeaderPage
from utils.add_product_to_cart_util import add_test_product_to_cart


def test_visual_cart(
    authenticated_page,
    config,
    image_snapshot,
    graphql_client,
    user_context,
    clear_cart_if_not_empty,
) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    cart = CartPage(page, config)

    # Add product using common utility
    add_test_product_to_cart(graphql_client, user_context)

    # Navigate to cart
    cart.navigate()

    # Hide badges for screenshot
    header.hide_vc_badge()

    # Take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/cart/cart_snapshots/cart_base.png", True)
