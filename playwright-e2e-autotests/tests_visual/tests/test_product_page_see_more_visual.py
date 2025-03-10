from PIL import Image
from io import BytesIO
from tests_visual.pages.product.product_page import ProductPage
from tests_visual.pages.header.header_page import HeaderPage
from utils.force_image_loading import force_image_loading

def test_visual_product_page(authenticated_page, config, image_snapshot) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    product = ProductPage(page, config)
    
    # Navigate to product page
    product.navigate()

    # Force image loading
    force_image_loading(page)
    header.hide_vc_badge()

    # Click property see more button
    product.click_see_more_button()

    # Click description see more button
    product.click_see_more_button()

    # Scroll back top
    product.scroll_to_top() 

    # Take a screenshot
    page.mouse.move(0, 0)
    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/product/product_page_snapshots/see_more/product_page_see_more_base.png", True) 