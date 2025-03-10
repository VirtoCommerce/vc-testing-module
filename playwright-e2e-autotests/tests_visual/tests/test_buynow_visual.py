from PIL import Image
from io import BytesIO
from tests_visual.pages.buynow.buynow_page import BuynowPage
from tests_visual.pages.header.header_page import HeaderPage
from utils.force_image_loading import force_image_loading


def test_visual_buynow(authenticated_page, config, image_snapshot) -> None:

    page = authenticated_page
    header = HeaderPage(page)
    buynow = BuynowPage(page, config)

    # Navigate to buynow page
    buynow.navigate()

    # Force immediate loading of all images
    force_image_loading(page)

    # Hide VC badge
    header.hide_vc_badge()

    # Mock product name and results count
    buynow.mock_product_name()
    buynow.mock_results_count()

    # Move mouse to top left corner
    page.mouse.move(0, 0)

    # Small wait to ensure all animations are complete
    page.wait_for_timeout(4000)

    # Take screenshot
    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/buynow/buynow_snapshots/buynow_base.png", True)
